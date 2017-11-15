import logging

from mock import Mock

from slippinj.cli.scripts.tables_configuration.tables_configuration import TablesConfiguration


class TestTablesConfiguration:
    def test_get_configuration_with_all_tables_as_incremental(self):
        mocked_table_configuration_generator = Mock()
        mocked_table_configuration_generator.get_table_configuration = Mock(return_value={})

        mocked_injector = Mock()
        mocked_injector.get = Mock(side_effect=[self.__generate_test_logger(), mocked_table_configuration_generator,
                                                mocked_table_configuration_generator])

        tables = {
            'tables': {
                'unit': {
                    'columns': [
                        {
                            'data_type': 'timestamp',
                            'column_name': 'column1'
                        }
                    ]
                },
                'test': {
                    'columns': [
                        {
                            'data_type': 'timestamp',
                            'column_name': 'column1'
                        }
                    ]
                }
            }
        }

        expected = {
            'incremental_tables': {
                'unit': { 'partition_field': 'column1'},
                'test': { 'partition_field': 'column1'}
            }
        }

        assert expected == TablesConfiguration().generate_configuration(tables, mocked_injector)

    def test_get_configuration_with_incremental_and_truncate_tables(self):
        mocked_incremental_table_configuration_generator = Mock()
        mocked_incremental_table_configuration_generator.get_table_configuration = Mock(return_value={})

        mocked_others_table_configuration_generator = Mock()
        mocked_others_table_configuration_generator.get_table_configuration = Mock(return_value={})

        mocked_injector = Mock()
        mocked_injector.get = Mock(
            side_effect=[self.__generate_test_logger(), mocked_incremental_table_configuration_generator,
                         mocked_others_table_configuration_generator])

        tables = {
            'tables': {
                'unit': {
                    'columns': [
                        {
                            'data_type': 'timestamp',
                            'column_name': 'column1'
                        }
                    ]
                },
                'test': {
                    'columns': [
                        {
                            'data_type': 'string',
                            'column_name': 'column1'
                        }
                    ]
                }
            }
        }

        expected = {
            'incremental_tables': {
                'unit': { 'partition_field': 'column1'}
            },
            'truncate_tables': {
                'test': {}
            }
        }

        assert expected == TablesConfiguration().generate_configuration(tables, mocked_injector)

    def __generate_test_logger(self):
        logger = logging.getLogger('test')
        logger.addHandler(logging.NullHandler())

        return logger
