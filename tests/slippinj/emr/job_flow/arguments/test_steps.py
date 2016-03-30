from slippinj.emr.job_flow.arguments.steps import StepsArgument


class TestStepsArgument(object):
    def test_parse_successfully_run(self):
        configuration = [
            {
                'name': 'name',
                'action_on_failure': 'action_on_failure',
                'jar': 'jar',
                'arguments': [
                    '1',
                    '2'
                ]
            }
        ]

        expected = {
            'Steps': [
                {
                    'Name': 'name',
                    'ActionOnFailure': 'action_on_failure',
                    'HadoopJarStep': {
                        'Jar': 'jar',
                        'Args': [
                            '1',
                            '2'
                        ]
                    }
                }
            ]
        }

        assert expected == StepsArgument().parse(configuration)
