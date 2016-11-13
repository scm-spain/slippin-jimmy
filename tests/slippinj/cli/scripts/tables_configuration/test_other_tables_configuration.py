from slippinj.cli.scripts.tables_configuration.other_tables_configuration import OtherTablesConfiguration


class TestOtherTablesConfiguration:
    def test_get_configuration_with_standard_table_structure(self):
        columns = [
            {'column_name': 'unit', 'data_type': 'string'},
            {'column_name': 'test', 'data_type': 'string'}
        ]

        expected = {
            'sqoop_options': {
                'm': '1',
                'map-column-hive': ''
            },
            'column_definition': {
                'columns': [
                    {'name': 'unit', 'type': 'string'},
                    {'name': 'test', 'type': 'string'}
                ]
            }
        }

        assert expected == OtherTablesConfiguration().get_table_configuration(columns)

    def test_get_configuration_with_columns_that_needs_mapping(self):
        columns = [
            {'column_name': 'timestamp_column', 'data_type': 'timestamp'},
            {'column_name': 'test', 'data_type': 'string'}
        ]

        expected = {
            'sqoop_options': {
                'm': '1',
                'map-column-hive': 'timestamp_column=timestamp',
            },
            'column_definition': {
                'columns': [
                    {'name': 'timestamp_column', 'type': 'timestamp'},
                    {'name': 'test', 'type': 'string'}
                ]
            }
        }

        assert expected == OtherTablesConfiguration().get_table_configuration(columns)
