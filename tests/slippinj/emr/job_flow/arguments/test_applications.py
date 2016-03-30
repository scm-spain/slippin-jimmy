from slippinj.emr.job_flow.arguments.applications import ApplicationsArgument


class TestApplicationsArgument(object):
    def test_parse_successfully_run(self):
        configuration = [
                'Hue',
                'Oozie-sandbox'
            ]

        expected = {
            'Applications': [
                {'Name': 'Hue'},
                {'Name': 'Oozie-sandbox'}
            ]
        }

        assert expected == ApplicationsArgument().parse(configuration)
