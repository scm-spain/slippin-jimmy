class StepsArgument(object):
    """Parse the steps argument"""

    def __init__(self):
        """
        Initialize the class
        """
        super(StepsArgument, self).__init__()

    def parse(self, configuration):
        """
        Parse steps from the configuration file and return it formatted
        :param configuration: dict
        :return: dict
        """
        steps = []

        for step in configuration:
            steps.append({
                'Name': step['name'],
                'ActionOnFailure': step['action_on_failure'],
                'HadoopJarStep': {
                    'Jar': step['jar'],
                    'Args': step['arguments']
                }
            })

        return {
            'Steps': steps
        }
