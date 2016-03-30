import logging

from mock import Mock

from slippinj.cli.scripts.scribe import Scribe


class TestScribe:
    def test_script_can_be_configured(self):
        mocked_args_parser = Mock()
        mocked_args_parser.add_parser = Mock(return_value=mocked_args_parser)
        mocked_args_parser.add_argument = Mock(return_value=True)

        Scribe(mocked_args_parser).configure()

        assert 13 == mocked_args_parser.add_argument.call_count

    def test_script_is_executable_only_excel_is_generated(self):
        mocked_db = Mock()
        mocked_db.get_all_tables_info = Mock(return_value={'tables': []})

        mocked_db_factory = Mock()
        mocked_db_factory.get_driver = Mock(return_value=mocked_db)

        mocked_excel_writer = Mock()
        mocked_excel_writer.generate_excel_file = Mock(return_value=True)

        mocked_yaml_configuration = Mock()
        mocked_yaml_configuration.generate_yaml_files = Mock(return_value=True)

        mocked_injector = Mock()
        mocked_injector.get = Mock(side_effect=[self.__get_logger(), mocked_db_factory, mocked_excel_writer, mocked_yaml_configuration])

        Scribe(Mock()).run(self.__generate_mocked_arguments(), mocked_injector)

        assert mocked_excel_writer.generate_excel_file.called
        assert mocked_db_factory.get_driver.called
        mocked_yaml_configuration.assert_not_called()

    def test_script_is_executable_generating_configuration_files(self):
        mocked_db = Mock()
        mocked_db.get_all_tables_info = Mock(return_value={'tables': []})

        mocked_db_factory = Mock()
        mocked_db_factory.get_driver = Mock(return_value=mocked_db)

        mocked_excel_writer = Mock()
        mocked_excel_writer.generate_excel_file = Mock(return_value=True)

        mocked_yaml_configuration = Mock()
        mocked_yaml_configuration.generate_yaml_files = Mock(return_value=True)

        logger = logging.getLogger('test')
        logger.addHandler(logging.NullHandler())

        mocked_injector = Mock()
        mocked_injector.get = Mock(side_effect=[self.__get_logger(), mocked_db_factory, mocked_excel_writer, mocked_yaml_configuration])

        mocked_args = self.__generate_mocked_arguments()
        mocked_args.excel_only = False

        Scribe(Mock()).run(mocked_args, mocked_injector)

        assert mocked_excel_writer.generate_excel_file.called
        assert mocked_db_factory.get_driver.called
        assert mocked_yaml_configuration.generate_yaml_files.called

    def __generate_mocked_arguments(self):
        mocked_args = Mock()
        mocked_args.db_driver = 'driver'
        mocked_args.db_host = 'host'
        mocked_args.db_user = 'user'
        mocked_args.db_pwd = 'password'
        mocked_args.db_port = 'port'
        mocked_args.db_name = 'name'
        mocked_args.table_list = 'unit,test'
        mocked_args.where = ''
        mocked_args.max_records = 10
        mocked_args.output = 'directory'
        mocked_args.excel_only = True

        return mocked_args

    def __get_logger(self):
        logger = logging.getLogger('test')
        logger.addHandler(logging.NullHandler())

        return logger

