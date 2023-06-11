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
        static_variables = [
            '+ ' + str(variable) for variable in self.variables if variable.static
        ]
        instance_variables = [
            '+ ' + str(variable) for variable in self.variables if not variable.static
        ]
        static_methods = [
            '+ ' + str(method) for method in self.methods if method.static
        ]
        instance_methods = [
            '+ ' + str(method) for method in self.methods if not method.static
        ]
        return 'class ' + \
            self.name + \
            ' {\n' + \
            ('\n'.join(static_variables) + '\n__\n' if static_variables else '') + \
            ('\n'.join(instance_variables) + '\n__\n' if instance_variables else '') + \
            ('\n'.join(static_methods) + '\n__\n' if static_methods else '') + \
            '\n'.join(instance_methods) + \
            '\n}'
