import glob
import os
import shutil
import tarfile
import tempfile
import time

from injector import inject


class Filesystem(object):
    """Manage the filesystem"""

    @inject(logger='logger')
    def __init__(self, logger):
        """
        Initialize the class
        :param logger: Logging
        """
        super(Filesystem, self).__init__()
        self.__tmp_dir = None
        self.__logger = logger

    def mkdir(self, output_dir):
        """
        Create a directory into filesystem
        :param output_dir: string
        :return: boolean
        """
        output_dir = os.path.dirname(output_dir)
        self.__logger.debug('Generating directory {output_dir}'.format(output_dir=output_dir))
        return os.mkdir(output_dir) if False == os.path.exists(output_dir) else True

    def write_file(self, output_file, content):
        """
        Write given content into file
        :param output_file: string
        :param content: string
        """
        self.mkdir(output_file)

        if isinstance(content,unicode):
            content = content.encode('utf-8')

        self.__logger.debug('Writing content into {output_file}'.format(output_file=output_file))
        f = open(output_file, 'w')
        f.write(content)
        f.close()

    def generate_temp_dir(self):
        """
        Generate a temporary directory and return the path to it
        :return: string
        """
        if not self.__tmp_dir:
            self.__tmp_dir = tempfile.mkdtemp()
        self.__logger.debug('Generating temporary directory')
        return self.__tmp_dir

    def remove_temp_dir(self):
        """
        Remove the temporary directory created using self.generate_temp_dir
        """
        if self.__tmp_dir:
            self.__logger.debug('Removing previously generated temporary directory')
            shutil.rmtree(self.__tmp_dir)

    def find_properties_file(self, wf_folder):
        """
        Find all the properties file inside the given folder
        :param wf_folder: string
        :return: list
        """
        self.__logger.debug('Scanning all properties files inside {folder}'.format(folder=wf_folder))
        return (
            glob.glob(os.path.join(wf_folder, '*.properties')) + glob.glob(
                os.path.join(wf_folder, '**', '*.properties')))

    def generate_tar_file(self, wf_folder, workflow_name=None):
        """
        Generate a tar file and compress inside all the workflow code, and returns the path to the newly created file
        :param wf_folder: string
        :param workflow_name: string
        :return: string
        """
        self.__logger.debug('Compressing {wf_folder} content inside tar file'.format(wf_folder=wf_folder))
        tar_filename = workflow_name + str(time.time()) + '.tar.gz'
        tar_name = os.path.join(wf_folder, tar_filename)
        tar = tarfile.open(name=tar_name, mode='w:gz')
        tar.add(wf_folder, arcname=workflow_name)
        tar.close()

        return os.path.join(wf_folder, tar_filename)
