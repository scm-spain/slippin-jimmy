import logging

import pytest
from mock import Mock

from slippinj.cli.scripts.tlacuilo import Tlacuilo
from slippinj.cli.objects.wf_configuration_object import WfConfigurationObject


class TestTlacuilo:
    def test_script_can_be_configured(self):
        mocked_args_parser = Mock()
        mocked_args_parser.add_parser = Mock(return_value=mocked_args_parser)
        mocked_args_parser.add_argument = Mock(return_value=True)

        Tlacuilo(mocked_args_parser).configure()

        assert 8 == mocked_args_parser.add_argument.call_count

    def test_script_raise_an_error_when_path_is_not_absolute(self):
        mocked_args = Mock()
        mocked_args.output_dir = '../path/to/code'

        with pytest.raises(IOError) as error:
            Tlacuilo(Mock()).run(mocked_args, Mock())

            assert 'Output directory should be an absolute path in order to save the files' == error.message

    def test_script_executes_successfully_without_extra_parameters_and_without_hive_templates(self):
        mocked_wf_templates_render = self.__get_mocked_templates_render()

        mocked_injector = Mock()
        mocked_injector.get = Mock(
            side_effect=[self.__generate_test_logger(), self.__get_mocked_wf_configuration(), mocked_wf_templates_render])

        Tlacuilo(Mock).run(self.__get_mocked_cli_arguments_without_extra_params(), mocked_injector)

        assert mocked_wf_templates_render.render_workflow_folder.called

    def test_script_executes_successfully_without_extra_parameters_and_with_hive_templates(self):
        mocked_wf_templates_render = self.__get_mocked_templates_render()
        mocked_hive_templates_render = self.__get_mocked_hive_templates_render()

        mocked_wf_configuration = self.__get_mocked_wf_configuration()
        mocked_wf_configuration.hive_template = 'test'

        mocked_injector = Mock()
        mocked_injector.get = Mock(
            side_effect=[self.__generate_test_logger(), mocked_wf_configuration, mocked_wf_templates_render,
                         mocked_hive_templates_render])

        Tlacuilo(Mock).run(self.__get_mocked_cli_arguments_without_extra_params(), mocked_injector)

        assert mocked_wf_templates_render.render_workflow_folder.called
        assert mocked_hive_templates_render.render_hive_folder.called

    def test_script_executes_successfully_with_extra_parameters_and_with_hive_templates(self):
        mocked_args = Mock()
        mocked_args.output_dir = '/path/to/code'
        mocked_args.configuration_file = 'configuration.test'
        mocked_args.extra = ['template=none', 'hive_template=none']
        mocked_args.template_dir = '/path/to/template'
        mocked_args.cluster_information = False

        mocked_wf_templates_render = self.__get_mocked_templates_render()
        mocked_hive_templates_render = self.__get_mocked_hive_templates_render()

        mocked_injector = Mock()
        mocked_injector.get = Mock(
            side_effect=[self.__generate_test_logger(), self.__get_mocked_wf_configuration(), mocked_wf_templates_render,
                         mocked_hive_templates_render])

        Tlacuilo(Mock).run(mocked_args, mocked_injector)

        assert mocked_wf_templates_render.render_workflow_folder.called
        assert mocked_hive_templates_render.render_hive_folder.called

    def __get_mocked_cli_arguments_without_extra_params(self):
        mocked_args = Mock()
        mocked_args.output_dir = '/path/to/code'
        mocked_args.configuration_file = 'configuration.test'
        mocked_args.extra = ''
        mocked_args.template_dir = '/path/to/template'
        mocked_args.cluster_information = False

        return mocked_args

    def __get_mocked_templates_render(self):
        mocked_wf_templates_render = Mock()
        mocked_wf_templates_render.render_workflow_folder = Mock(return_value=True)

        return mocked_wf_templates_render

    def __get_mocked_hive_templates_render(self):
        mocked_hive_templates_render = Mock()
        mocked_hive_templates_render.render_hive_folder = Mock(return_value=True)

        return mocked_hive_templates_render

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

        return wf_configuration
