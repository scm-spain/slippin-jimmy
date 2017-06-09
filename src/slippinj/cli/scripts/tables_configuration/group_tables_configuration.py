class GroupTablesConfiguration(object):
    def _is_mapping_needed(self, column_type):
        return column_type != 'string' and column_type != 'int'

    def _get_column_definition(self, column):

        column_definition_dict = {'name': column['column_name'], 'type': column['data_type']}
        if column['column_name'] != column['source_column_name']:
          column_definition_dict['source_name'] = column['source_column_name']
        return column_definition_dict
