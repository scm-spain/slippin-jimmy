from .group_tables_configuration import GroupTablesConfiguration


class IncrementalTablesConfiguration(GroupTablesConfiguration):
    """Generate the incremental tables configuration"""

    def __get_default_configuration(self):
        return {
            'sqoop_options': {
                'split-by': '',
                'where': '',
                'map-column-hive': '',
            },
            'column_definition': {
                'partition_column': 'dt',
                'column_split': '',
                'columns': []
            }
        }

    def get_table_configuration(self, columns):
        """
        Return configuration for given table, considering it is an incremental table
        :param columns: list
        :return: dict
        """
        table_configuration = self.__get_default_configuration()

        table_columns = []
        map_column_hive_fields_list = []
        for column in columns:
            if column['data_type'] == 'timestamp' and not table_configuration['sqoop_options']['split-by']:
                table_configuration['sqoop_options']['split-by'] = column['source_column_name']
                table_configuration['column_definition']['column_split'] = column['source_column_name']
                table_configuration['sqoop_options']['where'] = column['source_column_name'] + ' = \'${initDate}\''

            if self._is_mapping_needed(column['data_type']):
                map_column_hive_fields_list.append(column['source_column_name'] + '=' + column['data_type'])

            table_columns.append(self._get_column_definition(column))

        table_configuration['column_definition']['columns'] = table_columns
        table_configuration['sqoop_options']['map-column-hive'] = ','.join(map_column_hive_fields_list)

        if not table_configuration['sqoop_options']['split-by']:
            raise ValueError(
                'Given table can\'t be imported as incremental because no timestamp column has been found')

        return table_configuration
