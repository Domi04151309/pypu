from data.SourceFunction import SourceFunction


class SourceClass:
    def __init__(self) -> None:
        self.name: str = ''
        self.methods: list[SourceFunction] = []

    def __str__(self) -> str:
        return 'class ' + \
            self.name + \
            ' {\n' + \
            '\n'.join([str(method) for method in self.methods]) + \
            '\n}'
