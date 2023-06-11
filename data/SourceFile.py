from utils.PackageTools import get_matching_module
from .SourceClass import SourceClass
from .SourceFunction import SourceFunction
from .SourceVariable import SourceVariable


class SourceFile:
    """
    Data class representing a python file.
    """

    def __init__(self) -> None:
        self.name: str = ''
        self.imports: list[str] = []
        self.variables: list[SourceVariable] = []
        self.functions: list[SourceFunction] = []
        self.classes: list[SourceClass] = []

    def get_connection_strings(self) -> str:
        """
        Generates a valid PlantUML string for class associations.

        :return: A string describing associations between classes.
        """
        dependencies: list[str] = []
        imports: list[str] = self.imports
        # noinspection PyTypeChecker
        for item in self.variables + self.functions + self.classes:
            source_package = self.name + '.' + item.name + ' o--> '
            for dependency in item.get_dependencies():
                matching_module: str | None = get_matching_module(self.imports, dependency)
                if matching_module:
                    dependencies.append(source_package + matching_module)
                    if matching_module in imports:
                        imports.remove(matching_module)
        for item in self.classes:
            source_package = self.name + '.' + item.name + ' --|> '
            for base in item.bases:
                matching_module = get_matching_module(self.imports, base)
                if matching_module:
                    dependencies.append(source_package + matching_module)
                    if matching_module in imports:
                        imports.remove(matching_module)
        return '\n'.join(dependencies +
                         [self.name + ' ..> ' + source_import for source_import in imports])

    def __str__(self) -> str:
        return 'package ' + \
            self.name + \
            ' {\n' + \
            '\n'.join([
                'object "' + str(function) + '" as ' + function.name
                for function in self.functions
            ]) + \
            '\n' + \
            '\n'.join([
                'class "' + str(variable) + '" as ' + variable.name
                for variable in self.variables
            ]) + \
            '\n' + \
            '\n'.join([str(source_class) for source_class in self.classes]) + \
            '\n}'
