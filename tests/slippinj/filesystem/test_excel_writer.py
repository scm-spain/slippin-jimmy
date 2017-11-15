import logging

from mock import Mock

from slippinj.filesystem.excel_writer import ExcelWriter


class TestExcelWriter:
    def test_generate_excel_file_with_rows_information(self):
        mocked_count_sheet = Mock()
        mocked_count_sheet.append = Mock(return_value=True)

        mocked_tables_sheet = Mock()
        mocked_tables_sheet.append = Mock(return_value=True)

        mocked_rows_sheet = Mock()
        mocked_rows_sheet.append = Mock(return_value=True)

        mocked_workbook = Mock()
        mocked_workbook.create_sheet = Mock(side_effect=[mocked_count_sheet, mocked_tables_sheet, mocked_rows_sheet])
        mocked_workbook.save = Mock(return_value=True)

        mocked_filesystem = Mock()
        mocked_filesystem.mkdir = Mock(return_value=True)

        tables_information = {
            'unit': {
                'count': 1,
                'columns': [
                    {
                        'column_name': 'test_column',
                        'data_type': 'test_type',
                        'character_maximum_length': 1,
                        'is_nullable': False,
                        'column_default': 'testing'
                    }
                ],
                'rows': [
                    [
                        'row testing'
                    ]
                ]
            }
        }

        ExcelWriter(mocked_workbook, mocked_filesystem, self.__generate_test_logger()).generate_excel_file(tables_information, 'db_test', '/tmp')

        assert mocked_count_sheet.append.called
        assert 5 == mocked_tables_sheet.append.call_count
        assert 3 == mocked_rows_sheet.append.call_count

    def test_generate_excel_file_without_rows_information(self):
        mocked_count_sheet = Mock()
        mocked_count_sheet.append = Mock(return_value=True)

        mocked_tables_sheet = Mock()
        mocked_tables_sheet.append = Mock(return_value=True)

        mocked_rows_sheet = Mock()
        mocked_rows_sheet.append = Mock(return_value=True)

        mocked_workbook = Mock()
        mocked_workbook.create_sheet = Mock(side_effect=[mocked_count_sheet, mocked_tables_sheet, mocked_rows_sheet])
        mocked_workbook.save = Mock(return_value=True)

        mocked_filesystem = Mock()
        mocked_filesystem.mkdir = Mock(return_value=True)

        tables_information = {
            'unit': {
                'count': 1,
                'columns': [
                    {
                        'column_name': 'test_column',
                        'data_type': 'test_type',
                        'character_maximum_length': 1,
                        'is_nullable': False,
                        'column_default': 'testing'
                    }
                ]
            }
        }

        ExcelWriter(mocked_workbook, mocked_filesystem, self.__generate_test_logger()).generate_excel_file(tables_information, 'db_test', '/tmp')

        assert mocked_count_sheet.append.called
        assert 5 == mocked_tables_sheet.append.call_count
        assert False == mocked_rows_sheet.append.called

    def __generate_test_logger(self):
        logger = logging.getLogger('test')
        logger.addHandler(logging.NullHandler())

        return logger