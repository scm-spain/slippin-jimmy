import re

class TablesConfiguration(object):
    """Generate the tables configuration"""

    def __init__(self):
        """
        Initialize the class
        """
        self.INCREMENTAL_GROUP = 'incremental_tables'
        self.TRUNCATE_GROUP = 'truncate_tables'
        self.INCREMENTAL_COLUMN_TYPES = ['timestamp','date','datetime']

    def generate_configuration(self, tables_information, injector):
        """
        Generate the basic configuration given all the tables information
        :param tables_information: dict
        :param injector: Injector
        :return: dict
        """
        tables_data = {}

        logger = injector.get('logger')

        for table in tables_information['tables']:
            logger.debug('Generating configuration for table {table}'.format(table=table))

            table_configuration = {}

            for column in tables_information['tables'][table]['columns']:
                if any (column_type in column['data_type'] for column_type in self.INCREMENTAL_COLUMN_TYPES):
                    table_configuration['partition_field'] = column['column_name']
                    if not self.INCREMENTAL_GROUP in tables_data:
                        tables_data[self.INCREMENTAL_GROUP] = {}
                    tables_data[self.INCREMENTAL_GROUP][table] = table_configuration

            if not 'partition_field' in table_configuration:
                if not self.TRUNCATE_GROUP in tables_data:
                    tables_data[self.TRUNCATE_GROUP] = {}
                tables_data[self.TRUNCATE_GROUP][table] = table_configuration

        return tables_data
