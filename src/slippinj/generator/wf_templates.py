import os

from injector import inject


class WfTemplatesRender(object):
    """Proccess the templates to generate a whole Oozie Workflow using Jinja2 syntax"""

    @inject(templates_lib='templates_lib', filesystem='filesystem', logger='logger')
    def __init__(self, templates_lib, filesystem, logger):
        """
        Initialize the class
        :param templates_lib: TemplatesLib
        :param filesystem: Filesystem
        :param logger: Logging
        """
        super(WfTemplatesRender, self).__init__()

        self.__templates_lib = templates_lib
        self.__filesystem = filesystem
        self.__logger = logger

    def _generate_output_filename(self, filename, template_vars):
        self.__logger.debug('Output from WFTemplatesRender')
        return filename.replace('.j2', '')

    def __render_template_files(self, base_directory, output_folder, template_dir, template_vars, root_folder, files):
        files_output_folder = os.path.join(output_folder, os.path.basename(root_folder).replace(template_dir, ''))
        for template_file in files:
            self.__logger.debug('Rendering template file {template_file}'.format(template_file=template_file))
            full_template_file = os.path.join(root_folder.replace(base_directory, ''), template_file)

            output_file = os.path.join(files_output_folder, self._generate_output_filename(template_file, template_vars))
            self.__logger.debug('Writing rendered template into {output_file}'.format(output_file=output_file))
            self.__filesystem.write_file(
                output_file,
                self.__templates_lib.render(base_directory, full_template_file, template_vars)
            )

    def __get_template_files(self, base_directory, template_dir):
        self.__logger.debug('Getting templates from directory {base_directory}'.format(base_directory=base_directory))
        template_files = []

        for root, dirs, files in os.walk(os.path.join(base_directory, template_dir)):
            template_files.append({'files': files, 'root': root})

        return template_files

    def render_workflow_folder(self, base_directory, template_dir, output_folder, template_vars):
        """
        From the given template render all the files found inside and recreate the structure into output directory
        :param base_directory: string
        :param template_dir: string
        :param output_folder: string
        :param template_vars: dict
        """
        for template_files in self.__get_template_files(base_directory, template_dir):
            self.__render_template_files(
                base_directory,
                output_folder,
                template_dir,
                template_vars,
                template_files['root'],
                template_files['files']
            )
