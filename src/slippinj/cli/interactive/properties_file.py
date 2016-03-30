import os

from injector import inject


class PropertiesFile(object):
    """Get the properties file to run on the cluster"""

    @inject(filesystem='filesystem')
    def __init__(self, filesystem):
        """
        Initialize the class
        :param filesystem: Filesystem
        """
        super(PropertiesFile, self).__init__()

        self.__filesystem = filesystem

    def get(self, wf_dir):
        """
        Find all the properties file inside given workflow directory
        :param wf_dir: string
        :return: string
        """
        property_files = self.__filesystem.find_properties_file(wf_dir)

        print 'Properties files found:'
        print '[0] None'
        for index, property_file in enumerate(property_files):
            print '[{index}] {file}'.format(index=(index + 1), file=os.path.basename(property_file))

        file_to_run = int(raw_input('Select which file you would like to run: '))
        if file_to_run > 0:
            return property_files[(file_to_run - 1)]

        return False
