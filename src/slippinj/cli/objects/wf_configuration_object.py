class WfConfigurationObject(dict):
    """Stores the workflow configuration"""

    def __init__(self, configuration={}):
        dict.__init__(self, configuration)

    def __getattr__(self, item):
        try:
            return self.__getitem__(item)
        except KeyError:
            raise AttributeError(item)

    def __setattr__(self, item, value):
        if self.__dict__.has_key(item):
            dict.__setattr__(self, item, value)
        else:
            self.__setitem__(item, value)
