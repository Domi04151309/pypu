from utils.SourceClass import SourceClass
from utils.SourceFunction import SourceFunction


class SourceFile:
    def __init__(self) -> None:
        self.name: str = ''
        self.imports: list[str] = []
        self.functions: list[SourceFunction] = []
        self.classes: list[SourceClass] = []

    def get_connection_strings(self) -> str:
        return '\n'.join([self.name + ' ..> ' + source_import for source_import in self.imports])

    def __str__(self) -> str:
        return 'package ' + \
            self.name + \
            ' {\n' + \
            '\n'.join(['object "' + str(function) + '" as ' + function.name for function in self.functions]) + \
            '\n' + \
            '\n'.join([str(source_class) for source_class in self.classes]) + \
            '\n}'