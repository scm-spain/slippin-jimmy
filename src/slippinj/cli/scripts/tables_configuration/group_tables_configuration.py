class GroupTablesConfiguration(object):
    def _is_mapping_needed(self, column_type):
        return column_type != 'string' and column_type != 'int'

    def _get_column_definition(self, column):
        return {'name': column['column_name'], 'type': column['data_type']}
