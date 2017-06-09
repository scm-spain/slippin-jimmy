import os

from injector import inject


class ExcelWriter(object):
    """Generates the Excel files"""

    @inject(workbook='workbook', filesystem='filesystem', logger='logger')
    def __init__(self, workbook, filesystem, logger):
        """
        Initialize the class
        :param workbook: Workbook
        :param filesystem: Filesystem
        :param logger: Logging
        """
        super(ExcelWriter, self).__init__()
        self.__workbook = workbook
        self.__filesystem = filesystem
        self.__logger = logger

    def __init_count_sheet(self):

        count_sheet = self.__workbook.create_sheet('List & Count')
        return count_sheet

    def __init_tables_sheet(self):

        tables_sheet = self.__workbook.create_sheet('Tables information')
        return tables_sheet

    def __add_rows_sheet(self, table_name, columns, rows):

        rows_sheet = self.__workbook.create_sheet(table_name[:30])
        rows_sheet.append(['Table', table_name])
        rows_sheet.append(columns)

        for row in rows:
            try:
                rows_sheet.append(row)
            except:
                self.__logger.debug('PARSE ROW ERROR')
                rows_sheet.append(['PARSE ROW ERROR'])

    def generate_excel_file(self, tables_information, db_name, location):
        """
        Generate all the excel file content given tables list and save it into a location
        :param tables_information: dict
        :param db_name: string
        :param location: string
        :return: boolean
        """
        count_sheet = self.__init_count_sheet()
        tables_sheet = self.__init_tables_sheet()

        self.__logger.debug('Adding sheet with the table list and count for each table')
        count_sheet.append(['Database schema', 'Table name', '#rows'])
        for table_name in tables_information:
            count_sheet.append([db_name, table_name, tables_information[table_name]['count']])

            self.__logger.debug('Adding {table_name} table information'.format(table_name=table_name))
            tables_sheet.append([table_name])
            tables_sheet.append(['FIELD', 'TYPE', 'MAX_LENGTH', 'NULLABLE', 'DEFAULT VALUE'])

            columns = []
            for column in tables_information[table_name]['columns']:
                tables_sheet.append([column['source_column_name'], column['source_data_type'], column['character_maximum_length'],
                                     column['is_nullable'], column['column_default']])
                columns.append(column['source_column_name'])

            tables_sheet.append([])
            tables_sheet.append([])

            if 'rows' in tables_information[table_name] and tables_information[table_name]['rows']:
                self.__logger.debug('Adding rows information to {table_name} sheet'.format(table_name=table_name))
                self.__add_rows_sheet(table_name, columns, tables_information[table_name]['rows'])

        self.__filesystem.mkdir(location)
        self.__logger.debug('Saving excel file {db_name} into {location}'.format(db_name=db_name, location=location))
        return self.__workbook.save(os.path.join(location, db_name + '.xlsx'))
