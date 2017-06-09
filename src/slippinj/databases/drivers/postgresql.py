import psycopg2
import psycopg2.extras
import re
import unicodedata

from injector import inject, AssistedBuilder


class Postgresql(object):
    """Wrapper to connect to SQL Servers and get all the metastore information"""

    @inject(postgresql=AssistedBuilder(callable=psycopg2.connect), logger='logger')
    def __init__(self, postgresql, logger, db_host=None, db_user='root', db_name=None, db_schema=None, db_pwd=None, db_port=None):
        """
        Initialize the Postgresql driver to get all the tables information
        :param postgresql: Psycopg2
        :param logger: Logger
        :param db_host: string
        :param db_user: string
        :param db_name: string
        :param db_schema: string
        :param db_pwd: string
        :param db_port: int
        """
        super(Postgresql, self).__init__()

        self.__db_name = db_name
        self.__db_schema = db_schema if None != db_schema else 'public'
        self.__conn = postgresql.build(host=db_host, user=db_user, password=db_pwd, database=db_name,
                                  port=db_port if None != db_port else 5432)

        self.__column_types = {
            'timestamp without time zone': 'timestamp',
            'timestamp with time zone': 'timestamp',
            'uuid': 'string',
            'character': 'string',
            'character varying': 'string',
            'integer': 'int',
            'smallint': 'int',
            'text': 'string',
            'real': 'double',
            'numeric': 'double',
            'json': 'string',
            'USER-DEFINED': 'string'
        }

        self.__illegal_characters = re.compile(r'[\000-\010]|[\013-\014]|[\016-\037]|[\xa1]|[\xbf]|[\xc1]|[\xc9]|[\xcd]|[\xd1]|[\xbf]|[\xda]|[\xdc]|[\xe1]|[\xf1]|[\xfa]|[\xf3]')

        self.__logger = logger

    def __join_tables_list(self, tables):
        return ','.join('\'%s\'' % table for table in tables)

    def __get_valid_column_name(self, column_name):
        return re.sub("[ ,;{}()\n\t=]", "", column_name)

    def __get_table_list(self, table_list_query=False):

        self.__logger.debug('Getting table list')
        query = 'SELECT table_name FROM information_schema.tables WHERE table_catalog = %(db_name)s and table_schema = %(db_schema)s {table_list_query}'.format(
            table_list_query=' AND ' + table_list_query if table_list_query else '')
        cursor = self.__conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(query, {'db_name': self.__db_name, 'db_schema': self.__db_schema})

        self.__logger.debug('Found {count} tables'.format(count=cursor.rowcount))

        return map(lambda x: x[0], cursor.fetchall())

    def __get_tables_to_exclude(self, tables):
        return self.__get_table_list('table_name NOT IN ({tables})'.format(tables=self.__join_tables_list(tables)))

    def __get_database_collation(self):

        self.__logger.debug('Getting database collation')
        info_query = 'SELECT datcollate FROM pg_database WHERE datname = %(db_name)s'

        cursor = self.__conn.cursor()
        cursor.execute(info_query, {'db_name': self.__db_name})
        return cursor.fetchone()[0].lower()

    def __get_columns_for_tables(self, tables):

        self.__logger.debug('Getting columns information')
        info_query = 'SELECT table_name, column_name, data_type, character_maximum_length, is_nullable, column_default FROM information_schema.columns WHERE table_name IN ({tables}) AND table_catalog=%(db_name)s AND table_schema=%(db_schema)s'.format(
            tables=self.__join_tables_list(tables))

        cursor = self.__conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(info_query, {'db_name': self.__db_name, 'db_schema': self.__db_schema})

        tables_information = {}
        for row in cursor.fetchall():
            self.__logger.debug(
                'Columns found for table {table}'.format(table=row['table_name']))
            if not row['table_name'] in tables_information:
                tables_information[row['table_name']] = {'columns': []}

            tables_information[row['table_name']]['columns'].append({
                'source_column_name': row['column_name'],
                'column_name': self.__get_valid_column_name(row['column_name']),
                'source_data_type': row['data_type'],
                'data_type': row['data_type'] if row['data_type'] not in self.__column_types else self.__column_types[
                    row['data_type']],
                'character_maximum_length': row['character_maximum_length'],
                'is_nullable': row['is_nullable'],
                'column_default': row['column_default'],
            })

        return tables_information

    def __get_count_for_tables(self, tables):

        tables_information = {}
        cursor = self.__conn.cursor()
        for table in tables:
            try:
                self.__logger.debug('Getting count for table {table}'.format(table=table))
                info_query = 'SELECT COUNT(*) FROM {schema}.{table}'.format(table=table, schema=self.__db_schema)
                cursor.execute(info_query)
                tables_information[table] = {'count': cursor.fetchone()[0]}
            except:
                pass

        return tables_information

    def __get_top_for_tables(self, tables, top=30):

        tables_information = {}

        utf8_collation = ('utf-8' or 'utf8') in self.__get_database_collation()

        cursor = self.__conn.cursor()

        for table in tables:
            tables_information[table] = {'rows': []}
            if top > 0:
                try:
                    self.__logger.debug('Getting {top} rows for table {table}'.format(top=top, table=table))
                    info_query = 'SELECT * FROM {schema}.{table} LIMIT {top}'.format(top=top, table=table, schema=self.__db_schema)
                    cursor.execute(info_query)
                    for row in cursor.fetchall():
                        table_row = []
                        for column in row:
                            if not utf8_collation:
                                try:
                                    if type(column) is unicode:
                                        column = unicodedata.normalize('NFKD', column).encode('iso-8859-1', 'replace')
                                    else:
                                        column = str(column).decode('utf8', 'replace').encode('iso-8859-1', 'replace')
                                        if self.__illegal_characters.search(column):
                                            column = re.sub(self.__illegal_characters, '?', column)
                                except:
                                    column = 'Parse_error'
                            if column == 'None':
                                column = 'NULL'
                            table_row.append(column)

                        tables_information[table]['rows'].append(table_row)

                except psycopg2.ProgrammingError:
                    tables_information[table]['rows'].append(
                        'Error getting table data {error}'.format(error=psycopg2.ProgrammingError.message))

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
            tables = table_list.split(',')
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
