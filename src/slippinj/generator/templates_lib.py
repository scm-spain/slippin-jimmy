from injector import inject, AssistedBuilder
from jinja2 import Environment, FileSystemLoader


class TemplatesLib(object):
    """Manage all the templates library interaction"""

    @inject(loader=AssistedBuilder(FileSystemLoader), environment=AssistedBuilder(Environment))
    def __init__(self, loader, environment):
        """
        Initialize the class
        :param loader: FilesystemLoader
        :param environment: Environment
        """
        super(TemplatesLib, self).__init__()

        self.__loader = loader
        self.__environment = environment

    def __get_lib(self, base_directory):
        return self.__environment.build(
            loader=self.__loader.build(searchpath=base_directory),
            trim_blocks=True,
            extensions=['jinja2.ext.do']
        )

    def render(self, base_directory, template_file, template_vars):
        """
        Render the given template with the template_vars
        :param base_directory: string Path where the template can be found
        :param template_file: string
        :param template_vars: dict
        :return: string
        """
        return self.__get_lib(base_directory).get_template(template_file).render(template_vars)
