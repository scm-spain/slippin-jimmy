import re

class TablesConfiguration(object):
    """Generate the tables configuration"""

    def __init__(self):
        """
        Initialize the class
        """
        self.INCREMENTAL_GROUP = 'incremental_tables'
        self.OTHER_GROUP = 'other_tables'

    def __get_table_group(self, columns):
        for column in columns:
            if 'timestamp' == column['data_type']:
                return self.INCREMENTAL_GROUP

        return self.OTHER_GROUP

    def __get_valid_table_name(self, table_name):
        return re.sub("[^a-zA-Z0-9_]", "", table_name)


    def generate_configuration(self, tables_information, injector):
        """
        Generate the basic configuration given all the tables information
        :param tables_information: dict
        :param injector: Injector
        :return: dict
        """
        tables_data = {}

        logger = injector.get('logger')
        if 'excluded_tables' in tables_information and tables_information['excluded_tables']:
            logger.debug('Configuring excluded tables')
            tables_data['excluded_tables'] = tables_information['excluded_tables']

        for table in tables_information['tables']:
            logger.debug('Generating configuration for table {table}'.format(table=table))
            table_group = self.__get_table_group(tables_information['tables'][table]['columns'])
            if not table_group in tables_data:
                tables_data[table_group] = {}

            tables_data[table_group][table] = injector.get(
                table_group + '_configuration'
            ).get_table_configuration(tables_information['tables'][table]['columns'])

            valid_table_name = self.__get_valid_table_name(table)
            tables_data[table_group][valid_table_name] = tables_data[table_group].pop(table)

            if (valid_table_name != table):
              tables_data[table_group][valid_table_name]['source_table_name'] = table

        return tables_data
