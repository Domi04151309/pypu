from data.SourceClass import SourceClass
from data.SourceFunction import SourceFunction
from data.SourceVariable import SourceVariable


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

    def add_class_variable(
            self, source_class: str,
            variable: SourceVariable
    ) -> None:
        """
        Appends a variable to a source class.

        :param source_class: The class to append the variable to.
        :param variable: The variable to append.
        :return: Nothing.
        """
        for class_item in self.classes:
            if class_item.name == source_class:
                class_item.variables.append(variable)
                return

    def get_connection_strings(self) -> str:
        """
        Generates a valid PlantUML string for class associations.

        :return: A string describing associations between classes.
        """
        return '\n'.join([self.name + ' ..> ' + source_import for source_import in self.imports])

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
