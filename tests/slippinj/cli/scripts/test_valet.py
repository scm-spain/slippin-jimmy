import logging

from mock import Mock

from slippinj.cli.scripts.valet import Valet


class TestValet:
    def test_script_can_be_configured(self):
        mocked_args_parser = Mock()
        mocked_args_parser.add_parser = Mock(return_value=mocked_args_parser)
        mocked_args_parser.add_argument = Mock(return_value=True)

        Valet(mocked_args_parser).configure()

        assert 3 == mocked_args_parser.add_argument.call_count

    def test_script_is_executable(self):
        mocked_ansible_client = Mock()
        mocked_ansible_client.run_playbook = Mock(return_value=True)

        logger = logging.getLogger('test')
        logger.addHandler(logging.NullHandler())

        mocked_injector = Mock()
        mocked_injector.get = Mock('ansible_client', side_effect=[logger, mocked_ansible_client])

        mocked_args = Mock()
        mocked_args.playbook = 'test'
        mocked_args.cluster_id = 'test'

        assert None == Valet(Mock()).run(mocked_args, mocked_injector)
