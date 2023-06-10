from data.SourceFunction import SourceFunction
from data.SourceVariable import SourceVariable


class SourceClass:
    """
    Data class representing a python class.
    """

    def __init__(self) -> None:
        self.name: str = ''
        self.variables: list[SourceVariable] = []
        self.methods: list[SourceFunction] = []

    def __str__(self) -> str:
        self.variables.sort(key=lambda x: x.name)
        self.methods.sort(key=lambda x: x.name)
        return 'class ' + \
            self.name + \
            ' {\n' + \
            '\n'.join(['+ ' + str(variable) for variable in self.variables]) + \
            '\n' + \
            '__\n' + \
            '\n'.join(['+ ' + str(method) for method in self.methods if method.static]) + \
            '\n' + \
            '__\n' + \
            '\n'.join(['+ ' + str(method) for method in self.methods if not method.static]) + \
            '\n}'
