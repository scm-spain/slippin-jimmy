import logging
from mock import Mock, patch
from slippinj.databases.drivers.oracle import Oracle


class TestOracle:

    def setup_method(self, method):
        self.logger = logging.getLogger('test')

        self.logger.addHandler(logging.NullHandler())

    def teardown_method(self,method):
        self.logger = None

    @patch.object(Oracle, '_Oracle__makedict')
    def test_get_tables_info_when_no_table_list_is_provided(self,__makedict):

        __makedict.return_value = None

        mocked_table_list_query_cursor = Mock()
        mocked_table_list_query_cursor.execute = Mock(return_value=True)
        mocked_table_list_query_cursor.fetchall = Mock(return_value=[{'TABLE_NAME': 'unit'}, {'TABLE_NAME': 'test'}])

        mocked_table_count_query_cursor = Mock()
        mocked_table_count_query_cursor.execute = Mock(return_value=True)
        mocked_table_count_query_cursor.fetchone = Mock(return_value=[10])

        columns = {
            'TABLE_NAME': '',
            'COLUMN_NAME': 'column',
            'DATA_TYPE': 'string',
            'DATA_LENGTH': '1',
            'NULLABLE': 'N',
            'DATA_DEFAULT': ''
        }
        tables_columns = []
        columns.update(TABLE_NAME='unit')
        tables_columns.append(columns.copy())
        columns.update(TABLE_NAME='test')
        tables_columns.append(columns.copy())
        mocked_table_columns_query_cursor = Mock()
        mocked_table_columns_query_cursor.execute = Mock(return_value=True)
        mocked_table_columns_query_cursor.fetchall = Mock(return_value=tables_columns)

        mocked_table_top_query_cursor = Mock()
        mocked_table_top_query_cursor.execute = Mock(return_value=True)
        mocked_table_top_query_cursor.fetchall = Mock(return_value=[])

        mocked_oracle = Mock()
        mocked_oracle.cursor = Mock(side_effect=[mocked_table_list_query_cursor, mocked_table_count_query_cursor,
                                                mocked_table_columns_query_cursor, mocked_table_top_query_cursor])
        mocked_builder = Mock()
        mocked_builder.build = Mock(return_value=mocked_oracle)

        expected = {'tables': {'test': {'columns': [{'character_maximum_length': '1',
                                                     'column_default': '',
                                                     'column_name': 'column',
                                                     'data_type': 'string',
                                                     'is_nullable': 'N'}],
                                        'count': 10,
                                        'rows': []},
                               'unit': {'columns': [{'character_maximum_length': '1',
                                                     'column_default': '',
                                                     'column_name': 'column',
                                                     'data_type': 'string',
                                                     'is_nullable': 'N'}],
                                        'count': 10,
                                        'rows': []}},
                    'db_connection_string': 'jdbc:oracle:thin:@//test'
                    }

        assert expected == Oracle(mocked_builder, self.logger, db_host = 'test').get_all_tables_info(None, None, None)

    @patch.object(Oracle, '_Oracle__makedict')
    def test_get_tables_info_when_table_list_has_been_provided(self, __makedict):
        __makedict.return_value = None
        mocked_table_count_query_cursor = Mock()
        mocked_table_count_query_cursor.execute = Mock(return_value=True)
        mocked_table_count_query_cursor.fetchone = Mock(return_value=[10])

        columns = {
            'TABLE_NAME': '',
            'COLUMN_NAME': 'column',
            'DATA_TYPE': 'string',
            'DATA_LENGTH': '1',
            'NULLABLE': 'N',
            'DATA_DEFAULT': ''
        }
        tables_columns = []
        columns.update(TABLE_NAME='unit')
        tables_columns.append(columns.copy())
        columns.update(TABLE_NAME='test')
        tables_columns.append(columns.copy())
        mocked_table_columns_query_cursor = Mock()
        mocked_table_columns_query_cursor.execute = Mock(return_value=True)
        mocked_table_columns_query_cursor.fetchall = Mock(return_value=tables_columns)

        mocked_table_top_query_cursor = Mock()
        mocked_table_top_query_cursor.execute = Mock(return_value=True)
        mocked_table_top_query_cursor.fetchall = Mock(return_value=[])

        mocked_oracle = Mock()
        mocked_oracle.cursor = Mock(side_effect=[mocked_table_count_query_cursor, mocked_table_columns_query_cursor, mocked_table_top_query_cursor])
        mocked_builder = Mock()
        mocked_builder.build = Mock(return_value=mocked_oracle)

        expected = {'tables': {
            'unit': {'columns': [{'character_maximum_length': '1',
                                  'column_default': '',
                                  'column_name': 'column',
                                  'data_type': 'string',
                                  'is_nullable': 'N'}],
                     'count': 10,
                     'rows': []}},
                    'db_connection_string': 'jdbc:oracle:thin:@//test'
                    }

        assert expected == Oracle(mocked_builder, self.logger, db_host = 'test').get_all_tables_info('unit', None, None)
