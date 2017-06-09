from .group_tables_configuration import GroupTablesConfiguration


class OtherTablesConfiguration(GroupTablesConfiguration):
    """Generate the others tables configuration"""

    def __get_default_configuration(self):
        return {
            'sqoop_options': {
                'm': '1',
                'map-column-hive': ''
            },
            'column_definition': {
                'columns': []
            }
        }

    def get_table_configuration(self, columns):
        """
        Return configuration for given table, considering it is a table classified into others group
        :param columns: list
        :return: dict
        """
        table_configuration = self.__get_default_configuration()

        table_columns = []
        map_column_hive_fields_list = []
        for column in columns:
            if self._is_mapping_needed(column['data_type']):
                map_column_hive_fields_list.append(column['source_column_name'] + '=' + column['data_type'])

            table_columns.append(self._get_column_definition(column))

        table_configuration['column_definition']['columns'] = table_columns
        table_configuration['sqoop_options']['map-column-hive'] = ','.join(map_column_hive_fields_list)

        return table_configuration
