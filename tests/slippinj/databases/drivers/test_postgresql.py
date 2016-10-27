import logging

from mock import Mock

from slippinj.databases.drivers.postgresql import Postgresql

class TestPostgresql:
    def setup_method(self, method):
        self.logger = logging.getLogger('test')

        self.logger.addHandler(logging.NullHandler())

    def teardown_method(self, method):
        self.logger = None

    def test_get_tables_info_when_no_table_list_is_provided(self):
        mocked_table_list_query_cursor = Mock()
        mocked_table_list_query_cursor.execute = Mock(return_value=True)
        mocked_table_list_query_cursor.fetchall = Mock(return_value=[['unit'], ['test']])

        mocked_table_count_query_cursor = Mock()
        mocked_table_count_query_cursor.execute = Mock(return_value=True)
        mocked_table_count_query_cursor.fetchone = Mock(return_value=[10])

        columns = {
            'table_name': '',
            'column_name': 'column',
            'data_type': 'string',
            'character_maximum_length': '1',
            'is_nullable': 'NO',
            'column_default': ''
        }
        tables_columns = []
        columns.update(table_name='unit')
        tables_columns.append(columns.copy())
        columns.update(table_name='test')
        tables_columns.append(columns.copy())
        mocked_table_columns_query_cursor = Mock()
        mocked_table_columns_query_cursor.execute = Mock(return_value=True)
        mocked_table_columns_query_cursor.fetchall = Mock(return_value=tables_columns)

        mocked_table_collation_query_cursor = Mock()
        mocked_table_collation_query_cursor.execute = Mock(return_value=True)
        mocked_table_collation_query_cursor.fetchone = Mock(return_value=['en_US.UTF-8'])

        mocked_table_top_query_cursor = Mock()
        mocked_table_top_query_cursor.execute = Mock(return_value=True)
        mocked_table_top_query_cursor.fetchall = Mock(return_value=[])

        mocked_psycopg2 = Mock()
        mocked_psycopg2.cursor = Mock(side_effect=[mocked_table_list_query_cursor, mocked_table_count_query_cursor,
                                                mocked_table_columns_query_cursor, mocked_table_collation_query_cursor,
                                                mocked_table_top_query_cursor])
        mocked_builder = Mock()
        mocked_builder.build = Mock(return_value=mocked_psycopg2)

        expected = {'tables': {'test': {'columns': [{'character_maximum_length': '1',
                                                     'column_default': '',
                                                     'column_name': 'column',
                                                     'data_type': 'string',
                                                     'is_nullable': 'NO'}],
                                        'count': 10,
                                        'rows': []},
                               'unit': {'columns': [{'character_maximum_length': '1',
                                                     'column_default': '',
                                                     'column_name': 'column',
                                                     'data_type': 'string',
                                                     'is_nullable': 'NO'}],
                                        'count': 10,
                                        'rows': []}}}

        assert expected == Postgresql(mocked_builder, self.logger).get_all_tables_info(None, None, None)

    def test_get_tables_info_when_table_list_has_been_provided(self):
        mocked_table_list_query_cursor = Mock()
        mocked_table_list_query_cursor.execute = Mock(return_value=True)
        mocked_table_list_query_cursor.fetchall = Mock(return_value=[['test']])

        mocked_table_count_query_cursor = Mock()
        mocked_table_count_query_cursor.execute = Mock(return_value=True)
        mocked_table_count_query_cursor.fetchone = Mock(return_value=[10])

        columns = {
            'table_name': '',
            'column_name': 'column',
            'data_type': 'string',
            'character_maximum_length': '1',
            'is_nullable': 'NO',
            'column_default': ''
        }
        tables_columns = []
        columns.update(table_name='unit')
        tables_columns.append(columns.copy())
        columns.update(table_name='test')
        tables_columns.append(columns.copy())
        mocked_table_columns_query_cursor = Mock()
        mocked_table_columns_query_cursor.execute = Mock(return_value=True)
        mocked_table_columns_query_cursor.fetchall = Mock(return_value=tables_columns)

        mocked_table_collation_query_cursor = Mock()
        mocked_table_collation_query_cursor.execute = Mock(return_value=True)
        mocked_table_collation_query_cursor.fetchone = Mock(return_value=['en_US.UTF-8'])

        mocked_table_top_query_cursor = Mock()
        mocked_table_top_query_cursor.execute = Mock(return_value=True)
        mocked_table_top_query_cursor.fetchall = Mock(return_value=[])

        mocked_psycopg2 = Mock()
        mocked_psycopg2.cursor = Mock(side_effect=[mocked_table_list_query_cursor, mocked_table_count_query_cursor,
                                                mocked_table_columns_query_cursor, mocked_table_collation_query_cursor,
                                                mocked_table_top_query_cursor])
        mocked_builder = Mock()
        mocked_builder.build = Mock(return_value=mocked_psycopg2)

        expected = {'excluded_tables': ['test'], 'tables': {
            'unit': {'columns': [{'character_maximum_length': '1',
                                  'column_default': '',
                                  'column_name': 'column',
                                  'data_type': 'string',
                                  'is_nullable': 'NO'}],
                     'count': 10,
                     'rows': []}}}

        assert expected == Postgresql(mocked_builder, self.logger).get_all_tables_info('unit', None, None)
