class TagsArgument(object):
    """Parse the tags argument"""

    def __init__(self):
        """
        Initialize the class
        """
        super(TagsArgument, self).__init__()

    def parse(self, configuration):
        """
        Parse tags from the configuration file and return it formatted
        :param configuration: dict
        :return: dict
        """
        return {
            'Tags': [{'Key': tag, 'Value': configuration[tag]} for tag in configuration]
        }
