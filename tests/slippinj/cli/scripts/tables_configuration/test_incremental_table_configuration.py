from slippinj.cli.scripts.tables_configuration.incremental_table_configuration import IncrementalTablesConfiguration
import pytest


class TestIncrementalTablesConfiguration:
    def test_get_configuration_with_standard_table_structure(self):
        columns = [
            {'column_name': 'unit', 'data_type': 'timestamp'},
            {'column_name': 'test', 'data_type': 'string'}
        ]

        expected = {
            'sqoop_options': {
                'split-by': 'unit',
                'where': 'unit = \'${initDate}\'',
                'map-column-hive': 'unit=timestamp',
            },
            'column_definition': {
                'partition_column': 'dt',
                'column_split': 'unit',
                'columns': [
                    {'name': 'unit', 'type': 'timestamp'},
                    {'name': 'test', 'type': 'string'}
                ]
            }
        }

        assert expected == IncrementalTablesConfiguration().get_table_configuration(columns)

    def test_get_configuration_with_two_timestamp_columns_defined(self):
        columns = [
            {'column_name': 'timestamp_column_1', 'data_type': 'timestamp'},
            {'column_name': 'timestamp_column_2', 'data_type': 'timestamp'},
            {'column_name': 'test', 'data_type': 'string'}
        ]

        expected = {
            'sqoop_options': {
                'split-by': 'timestamp_column_1',
                'where': 'timestamp_column_1 = \'${initDate}\'',
                'map-column-hive': 'timestamp_column_1=timestamp,timestamp_column_2=timestamp',
            },
            'column_definition': {
                'partition_column': 'dt',
                'column_split': 'timestamp_column_1',
                'columns': [
                    {'name': 'timestamp_column_1', 'type': 'timestamp'},
                    {'name': 'timestamp_column_2', 'type': 'timestamp'},
                    {'name': 'test', 'type': 'string'}
                ]
            }
        }

        assert expected == IncrementalTablesConfiguration().get_table_configuration(columns)

    def test_get_configuration_without_timestamp_column_defined(self):
        columns = [
            {'column_name': 'unit', 'data_type': 'string'},
            {'column_name': 'test', 'data_type': 'string'}
        ]

        with pytest.raises(ValueError) as value_error:
            IncrementalTablesConfiguration().get_table_configuration(columns)

        assert 'Given table can\'t be imported as incremental because not timestamp column has been found' == str(
            value_error.value)
