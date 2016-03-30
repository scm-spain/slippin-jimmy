import logging

from mock import Mock

from slippinj.generator.wf_templates import WfTemplatesRender


class TestWfTemplatesRender:
    def test_workflow_folder_can_be_rendered_successfully(self, tmpdir):
        mocked_fs = Mock()
        mocked_fs.write_file = Mock(return_value=True)

        mocked_templates_lib = Mock()
        mocked_templates_lib.render = Mock(return_value=True)

        d = tmpdir.mkdir('test')
        t = d.join('template.j2')
        t.write('content of the template')

        logger = logging.getLogger('test')
        logger.addHandler(logging.NullHandler())

        WfTemplatesRender(mocked_templates_lib, mocked_fs, logger).render_workflow_folder(str(d.realpath()), '', 'output',
                                                                                  {})
        assert 1 == mocked_fs.write_file.call_count
        assert 1 == mocked_templates_lib.render.call_count
