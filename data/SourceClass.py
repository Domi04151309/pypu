from data.SourceFunction import SourceFunction
from data.SourceVariable import SourceVariable


class SourceClass:
    def __init__(self) -> None:
        self.name: str = ''
        self.variables: list[SourceVariable] = []
        self.methods: list[SourceFunction] = []

    def __str__(self) -> str:
        return 'class ' + \
            self.name + \
            ' {\n' + \
            '\n'.join([str(variable) for variable in self.variables]) + \
            '\n' + \
            '\n'.join([str(method) for method in self.methods]) + \
            '\n}'
