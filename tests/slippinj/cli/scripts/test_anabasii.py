import logging

from mock import Mock

from slippinj.cli.objects.wf_configuration_object import WfConfigurationObject
from slippinj.cli.scripts.anabasii import Anabasii


class TestAnabasii:
    def test_script_can_be_configured(self):
        mocked_args_parser = Mock()
        mocked_args_parser.add_parser = Mock(return_value=mocked_args_parser)
        mocked_args_parser.add_argument = Mock(return_value=True)

        Anabasii(mocked_args_parser).configure()

        assert 4 == mocked_args_parser.add_argument.call_count

    def test_script_is_executable_when_cluster_id_has_not_been_provided_not_standalone_run(self):
        mocked_interactive_cluster_id = Mock()
        mocked_interactive_cluster_id.get = Mock(return_value=True)

        mocked_emr_deploy = Mock()
        mocked_emr_deploy.upload_code = Mock(return_value=True)

        mocked_injector = Mock()
        mocked_injector.get = Mock(
            side_effect=[self.__generate_test_logger(), self.__get_mocked_wf_configuration(),
                            mocked_interactive_cluster_id, mocked_emr_deploy])

        mocked_args = Mock()
        mocked_args.cluster_id = False
        mocked_args.wf_dir = 'test'
        mocked_args.hdfs_deploy_folder = 'test'
        mocked_args.local_mode = False
        mocked_args.script = 'hersir'

        Anabasii(Mock()).run(mocked_args, mocked_injector)

        assert mocked_interactive_cluster_id.get.called

    def test_script_is_executable_when_cluster_id_has_not_been_provided_but_added_on_config_not_standalone_run(self):
        mocked_interactive_cluster_id = Mock()
        mocked_interactive_cluster_id.get = Mock(return_value=True)

        mocked_emr_deploy = Mock()
        mocked_emr_deploy.upload_code = Mock(return_value=True)

        mocked_injector = Mock()
        mocked_injector.get = Mock(
            side_effect=[self.__generate_test_logger(), self.__get_mocked_wf_configuration_with_cluster_properties(),
                            mocked_emr_deploy])

        mocked_args = Mock()
        mocked_args.cluster_id = False
        mocked_args.wf_dir = 'test'
        mocked_args.hdfs_deploy_folder = 'test'
        mocked_args.local_mode = False
        mocked_args.script = 'hersir'

        Anabasii(Mock()).run(mocked_args, mocked_injector)

        assert not mocked_interactive_cluster_id.get.called

    def test_script_is_executable_when_cluster_id_has_not_been_provided_standalone_run(self):
        mocked_interactive_cluster_id = Mock()
        mocked_interactive_cluster_id.get = Mock(return_value=True)

        mocked_emr_deploy = Mock()
        mocked_emr_deploy.upload_code = Mock(return_value=True)

        mocked_injector = Mock()
        mocked_injector.get = Mock(
            side_effect=[self.__generate_test_logger(), mocked_interactive_cluster_id, mocked_emr_deploy])

        mocked_args = Mock()
        mocked_args.cluster_id = False
        mocked_args.wf_dir = 'test'
        mocked_args.hdfs_deploy_folder = 'test'
        mocked_args.local_mode = False
        mocked_args.script = 'anabasii'

        Anabasii(Mock()).run(mocked_args, mocked_injector)

        assert mocked_interactive_cluster_id.get.called

    def test_script_is_executable_when_cluster_id_has_been_provided_not_standalone_run(self):
        mocked_interactive_cluster_id = Mock()
        mocked_interactive_cluster_id.get = Mock(return_value=True)

        mocked_emr_deploy = Mock()
        mocked_emr_deploy.upload_code = Mock(return_value=True)

        mocked_injector = Mock()
        mocked_injector.get = Mock(
            side_effect=[self.__generate_test_logger(), self.__get_mocked_wf_configuration(), mocked_emr_deploy])

        mocked_args = Mock()
        mocked_args.cluster_id = 'test'
        mocked_args.wf_dir = 'test'
        mocked_args.hdfs_deploy_folder = 'test'
        mocked_args.local_mode = False
        mocked_args.script = 'hersir'

        Anabasii(Mock()).run(mocked_args, mocked_injector)

        mocked_interactive_cluster_id.get.assert_not_called()
        assert mocked_emr_deploy.upload_code.called

    def test_script_is_executable_when_cluster_id_has_been_provided_standalone_run(self):
        mocked_interactive_cluster_id = Mock()
        mocked_interactive_cluster_id.get = Mock(return_value=True)

        mocked_emr_deploy = Mock()
        mocked_emr_deploy.upload_code = Mock(return_value=True)


        mocked_injector = Mock()
        mocked_injector.get = Mock(
            side_effect=[self.__generate_test_logger(), mocked_emr_deploy])

        mocked_args = Mock()
        mocked_args.cluster_id = 'test'
        mocked_args.wf_dir = 'test'
        mocked_args.hdfs_deploy_folder = 'test'
        mocked_args.local_mode = False
        mocked_args.script = 'anabasii'

        Anabasii(Mock()).run(mocked_args, mocked_injector)

        mocked_interactive_cluster_id.get.assert_not_called()
        assert mocked_emr_deploy.upload_code.called

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

        return wf_configuration

    def __get_mocked_wf_configuration_with_cluster_properties(self):
        wf_configuration = WfConfigurationObject()
        wf_configuration.output_directory = 'test'
        wf_configuration.wf_dir = 'test'
        wf_configuration.template = 'test'
        wf_configuration.incremental_tables = []
        wf_configuration.hdfs_deploy_folder = 'test'
        wf_configuration.cluster_id = 'test'

        return wf_configuration
