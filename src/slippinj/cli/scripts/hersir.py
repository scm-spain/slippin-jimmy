from .anabasii import Anabasii
from .basic_script import BasicScript
from .cooper import Cooper
from .tlacuilo import Tlacuilo


class Hersir(BasicScript):
    """Run all the steps to compile, upload and run a workflow to a running cluster"""

    def __get_scripts(self):
        return [
            Tlacuilo(self._parser),
            Anabasii(self._parser),
            Cooper(self._parser)
        ]

    def get_arguments(self):
        """
        Get the arguments to configure current script
        :return: list
        """
        arguments = []
        for script in self.__get_scripts():
            arguments.extend(script.get_arguments())

        return arguments

    def run(self, args, injector):
        """
        Run the steps in order to compile, upload and run a workflow
        :param args: Namespace
        :param injector: Injector
        """
        for script in self.__get_scripts():
            script.run(args, injector)
