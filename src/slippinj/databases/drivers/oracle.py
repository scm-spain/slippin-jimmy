import re
import unicodedata
from injector import inject, AssistedBuilder
import cx_Oracle as pyoracle


class Oracle(object):
    """Wrapper to connect to Oracle Servers and get all the metastore information"""

    @inject(oracle=AssistedBuilder(callable=pyoracle.connect), logger='logger')
    def __init__(self, oracle, logger, db_host=None, db_user='root', db_name=None, db_schema=None, db_pwd=None, db_port=None):

        super(Oracle, self).__init__()

        self.__db_name = db_name
        self.__db_user = db_user
        self.__db_dsn = pyoracle.makedsn(host=db_host, port=int(db_port) if None != db_port else 1521, service_name=db_name)
        self.__conn = oracle.build(user=db_user, password=db_pwd, dsn=self.__db_dsn)

        self.__column_types = {
            'NUMBER': 'double',
            'BINARY_DOUBLE': 'double',
            'BINARY_FLOAT': 'float',
            'CHAR': 'string',
            'NCHAR': 'string',
            'VARCHAR2': 'string',
            'NVARCHAR2': 'string',
            'DATE': 'timestamp',
            'TIMESTAMP': 'timestamp',
            'RAW': 'binary',
        }

        self.__illegal_characters = re.compile(r'[\000-\010]|[\013-\014]|[\016-\037]|[\xa1]|[\xc1]|[\xc9]|[\xcd]|[\xd1]|[\xbf]|[\xda]|[\xdc]|[\xe1]|[\xf1]|[\xfa]|[\xf3]')

        self.__logger = logger

    def __makedict(self,cursor):
        """
        Convert cx_oracle query result to be a dictionary
        """

        cols = [d[0] for d in cursor.description]

        def createrow(*args):
            return dict(zip(cols, args))

        return createrow

    def __join_tables_list(self, tables):
            return ','.join('\'%s\'' % table for table in tables)

    def __get_valid_column_name(self, column_name):
        return re.sub("[ ,;{}()\n\t=]", "", column_name)

    def __get_table_list(self, table_list_query=False):
        self.__logger.debug('Getting table list')
        query = "SELECT DISTINCT table_name " \
                "FROM all_tables " \
                "WHERE OWNER NOT LIKE '%SYS%' " \
                "AND OWNER NOT LIKE 'APEX%' " \
                "AND OWNER NOT LIKE 'XDB' {table_list_query}".format(table_list_query=' AND ' + table_list_query if table_list_query else '')

        cursor = self.__conn.cursor()
        cursor.execute(query)
        cursor.rowfactory = self.__makedict(cursor)

        tablelist = map(lambda x: x['TABLE_NAME'], cursor.fetchall())
        self.__logger.debug('Found {count} tables'.format(count=cursor.rowcount))

        return tablelist

    def __get_tables_to_exclude(self, tables):
        return self.__get_table_list('table_name NOT IN ({tables})'.format(tables=self.__join_tables_list(tables)))

    def __get_columns_for_tables(self, tables):
        self.__logger.debug('Getting columns information')
        info_query = "SELECT table_name, column_name, data_type, data_length, nullable, data_default " \
                     "FROM ALL_TAB_COLS " \
                     "WHERE table_name IN ({tables}) " \
                     "ORDER BY COLUMN_ID".format(tables=self.__join_tables_list(tables))

        cursor = self.__conn.cursor()
        cursor.execute(info_query)
        cursor.rowfactory = self.__makedict(cursor)

        tables_information = {}
        for row in cursor.fetchall():
            self.__logger.debug('Columns found for table {table}'.format(table=row['TABLE_NAME']))
            if not row['TABLE_NAME'] in tables_information:
                tables_information[row['TABLE_NAME']] = {'columns': []}
            tables_information[row['TABLE_NAME']]['columns'].append({
                'source_column_name': row['COLUMN_NAME'],
                'column_name': self.__get_valid_column_name(row['COLUMN_NAME']),
                'source_data_type': row['DATA_TYPE'],
                'data_type': row['DATA_TYPE'].lower() if row['DATA_TYPE'] not in self.__column_types else self.__column_types[
                    row['DATA_TYPE']],
                'character_maximum_length': row['DATA_LENGTH'],
                'is_nullable': row['NULLABLE'],
                'column_default': row['DATA_DEFAULT'],
            })

        return tables_information

    def __get_count_for_tables(self, tables):

        tables_information = {}
        cursor = self.__conn.cursor()
        for table in tables:
            try:
                self.__logger.debug('Getting count for table {table}'.format(table=table))
                info_query = 'SELECT COUNT(*) FROM {table}'.format(table=table)
                cursor.execute(info_query)
                tables_information[table] = {'count': cursor.fetchone()[0]}
            except:
                self.__logger.debug('The count query for table {table} has fail'.format(table=table))
                pass

        return tables_information

    def __get_top_for_tables(self, tables, top=30):

        tables_information = {}

        cursor = self.__conn.cursor()
        for table in tables:
            tables_information[table] = {'rows': []}
            if top > 0:
                try:
                    self.__logger.debug('Getting {top} rows for table {table}'.format(top=top, table=table))
                    query = 'SELECT * FROM {table} WHERE ROWNUM < {top}'.format(top=top, table=table)
                    cursor.execute(query)
                    for row in cursor.fetchall():
                        table_row = []
                        for column in row:
                            try:
                                if type(column) is unicode:
                                    column = unicodedata.normalize('NFKD', column).encode('iso-8859-1', 'replace')

                                else:
                                    column = str(column).decode('utf8', 'replace').encode('iso-8859-1', 'replace')
                                    if self.__illegal_characters.search(column):
                                        column = re.sub(self.__illegal_characters, '?', column)

                                if column == 'None':
                                    column = 'NULL'

                            except:
                                column = 'Parse_error'

                            table_row.append(column)

                        tables_information[table]['rows'].append(table_row)

                except pyoracle.ProgrammingError:
                    tables_information[table]['rows'].append(
                        'Error getting table data {error}'.format(error=pyoracle.ProgrammingError.message))

        return tables_information

    def get_all_tables_info(self, table_list, table_list_query, top_max):
        """
        Return all the tables information reading from the Information Schema database
        :param table_list: string
        :param table_list_query: string
        :param top_max: integer
        :return: dict
        """
        tables_to_exclude = {}

        if table_list:
            tables = map(lambda x: unicode(x), table_list.split(','))
            tables_to_exclude = self.__get_tables_to_exclude(tables)
        else:
            tables = self.__get_table_list(table_list_query)

        tables_counts = self.__get_count_for_tables(tables)
        tables_columns = self.__get_columns_for_tables(tables)
        tables_top = self.__get_top_for_tables(tables, top_max)
        tables_info = {'tables': {}}
        for table in tables_counts:
            tables_info['tables'][table] = {}
            tables_info['tables'][table].update(tables_columns[table])
            tables_info['tables'][table].update(tables_counts[table])
            tables_info['tables'][table].update(tables_top[table])

        if tables_to_exclude:
            tables_info['excluded_tables'] = tables_to_exclude

        return tables_info

