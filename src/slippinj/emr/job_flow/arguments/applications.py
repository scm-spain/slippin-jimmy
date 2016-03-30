class ApplicationsArgument(object):
    """Parse the applications argument"""

    def __init__(self):
        """
        Initialize the class
        """
        super(ApplicationsArgument, self).__init__()

    def parse(self, configuration):
        """
        Parse applications from the configuration file and return it formatted
        :param configuration: dict
        :return: dict
        """

        return {
            'Applications': [{'Name': v} for v in configuration]
        }
