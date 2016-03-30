class TablesConfiguration(object):
    """Generate the tables configuration"""

    def __init__(self):
        """
        Initialize the class
        """
        self.INCREMENTAL_GROUP = 'incremental'
        self.OTHERS_GROUP = 'others'

    def __get_table_group(self, columns):
        for column in columns:
            if 'timestamp' == column['data_type']:
                return self.INCREMENTAL_GROUP

        return self.OTHERS_GROUP

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
                table_group + '_table_configuration'
            ).get_table_configuration(tables_information['tables'][table]['columns'])

        return tables_data
