from string import Template

from ..generator.wf_templates import WfTemplatesRender


class HiveTemplatesRender(WfTemplatesRender):
    """Process templates to generate custom Hive scripts"""

    def _generate_output_filename(self, filename, template_vars):
        return Template(filename).substitute(template_vars).replace('.j2', '')

    def render_hive_folder(self, template_dir, template, output_folder, tables_configuration):
        """
        Render all the templates related to hive
        :param template_dir: string
        :param template: string
        :param output_folder: string
        :param tables_configuration: dict
        """
        for table_name in tables_configuration:
            tables_configuration[table_name]['table_name'] = table_name
            self.render_workflow_folder(template_dir, template, output_folder, tables_configuration[table_name])
