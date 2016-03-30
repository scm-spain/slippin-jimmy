from slippinj.emr.job_flow.arguments.tags import TagsArgument


class TestTagsArgument(object):
    def test_parse_successfully_run(self):
        configuration = {
            'environment': 'devel',
            'type': 'test'
        }

        expected = {
            'Tags': [
                {
                    'Key': 'environment',
                    'Value': 'devel'
                },
                {
                    'Key': 'type',
                    'Value': 'test'
                },
            ]
        }

        assert expected == TagsArgument().parse(configuration)
