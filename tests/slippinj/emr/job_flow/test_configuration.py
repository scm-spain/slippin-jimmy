import pytest

from slippinj.emr.job_flow.configuration import JobFlowConfigurationParser


class TestJobFlowConfigurationParser(object):
    def setup_method(self, method):
        self.__job_flow_configuration = JobFlowConfigurationParser()

    def teardown_method(self, method):
        self.__job_flow_configuration = None

    def test_valid_configuration(self):
        configuration = {
            'name': 'test',
            'release_label': 'test',
            'availability_zone': 'test',
            'instances': {
                'ec2_key_name': 'test',
                'master': {},
                'core': {}
            },
            'tags': []
        }

        assert True == self.__job_flow_configuration.validate(configuration)

    def test_invalid_configuration_in_parent_keys(self):
        configuration = {
            'name': 'test',
            'availability_zone': 'test',
            'instances': {
                'ec2_key_name': 'test',
                'master': {},
                'core': {}
            },
            'tags': []
        }

        with pytest.raises(AttributeError) as e:
            self.__job_flow_configuration.validate(configuration)
            assert 'release_label not found in configuration file' in str(e.value)

    def test_invalid_configuration_in_children_keys(self):
        configuration = {
            'name': 'test',
            'release_label': 'test',
            'availability_zone': 'test',
            'instances': {
                'ec2_key_name': 'test',
                'core': {}
            },
            'tags': []
        }

        with pytest.raises(AttributeError) as e:
            self.__job_flow_configuration.validate(configuration)
            assert 'instances.master not found in configuration file' in str(e.value)
