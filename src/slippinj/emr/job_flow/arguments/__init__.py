import os

__all__ = []
for module in os.listdir(os.path.dirname(__file__)):
    if module == '__init__.py' or module[-3:] != '.py':
        continue
    __import__(module[:-3], locals(), globals())
    __all__.append(module[:-3])
del module


def parser_exists(argument_type):
    return argument_type in __all__


def get_parser(argument_type):
    return eval(argument_type + '.' + argument_type.capitalize() + 'Argument()')
