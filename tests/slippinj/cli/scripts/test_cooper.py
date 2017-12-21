import logging

from mock import Mock

from slippinj.cli.objects.wf_configuration_object import WfConfigurationObject
from slippinj.cli.scripts.cooper import Cooper


class TestCooper:
    def test_script_can_be_configured(self):
        mocked_args_parser = Mock()
        mocked_args_parser.add_parser = Mock(return_value=mocked_args_parser)
        mocked_args_parser.add_argument = Mock(return_value=True)

        Cooper(mocked_args_parser).configure()

        assert 3 == mocked_args_parser.add_argument.call_count

    def test_script_is_executable_successfully(self):
        mocked_interactive_properties_file = Mock()
        mocked_interactive_properties_file.get = Mock(return_value=True)

        mocked_emr_deploy = Mock()
        mocked_emr_deploy.run_properties_file = Mock(return_value=True)

        mocked_injector = Mock()
        mocked_injector.get = Mock(
            side_effect=[self.__get_mocked_wf_configuration(), mocked_interactive_properties_file,
                         self.__generate_test_logger(), mocked_emr_deploy])

        mocked_args = Mock()
        mocked_args.wf_dir = 'test'
        mocked_args.cluster_id = 'test'
        mocked_args.job_file_name = False

        Cooper(Mock()).run(mocked_args, mocked_injector)

        assert mocked_emr_deploy.run_properties_file.called

    def test_script_execution_when_no_properties_file_is_selected(self):
        mocked_interactive_properties_file = Mock()
        mocked_interactive_properties_file.get = Mock(return_value=False)

        mocked_emr_deploy = Mock()
        mocked_emr_deploy.run_properties_file = Mock(return_value=True)

        mocked_injector = Mock()
        mocked_injector.get = Mock(
            side_effect=[self.__get_mocked_wf_configuration(), mocked_interactive_properties_file,
                         self.__generate_test_logger(), mocked_emr_deploy])

        mocked_args = Mock()
        mocked_args.wf_dir = 'test'
        mocked_args.cluster_id = 'test'
        mocked_args.job_file_name = False

        mocked_emr_deploy.run_properties_file.assert_not_called()

    def __generate_test_logger(self):
        logger = logging.getLogger('test')
        logger.addHandler(logging.NullHandler())

        return logger

    def __get_mocked_wf_configuration(self):
        wf_configuration = WfConfigurationObject()
        wf_configuration.output_directory = 'test'
        wf_configuration.wf_dir = 'test'
        wf_configuration.template = 'test'
        wf_configuration.incremental_tables = []
        wf_configuration.hdfs_deploy_folder = 'test'
        wf_configuration.cluster_id = 'test'

        return wf_configuration
