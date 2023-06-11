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
        static_variables = '\n'.join([
            '+ ' + str(variable) for variable in self.variables if variable.static
        ])
        instance_variables = '\n'.join([
            '+ ' + str(variable) for variable in self.variables if not variable.static
        ])
        static_methods = '\n'.join([
            '+ ' + str(method) for method in self.methods if method.static
        ])
        instance_methods = '\n'.join([
            '+ ' + str(method) for method in self.methods if not method.static
        ])
        return 'class ' + \
            self.name + \
            ' {\n' + \
            '\n__\n'.join([
                x
                for x in [static_variables, instance_variables, static_methods, instance_methods]
                if x
            ]) + \
            '\n}'
