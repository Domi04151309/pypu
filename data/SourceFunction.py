from data.SourceVariable import SourceVariable


class SourceFunction:
    def __init__(self) -> None:
        self.static = False
        self.name: str = ''
        self.params: list[SourceVariable] = []
        self.returns: str = 'Any'

    def __str__(self) -> str:
        return ('{static}' if self.static else '') + \
            self.name + \
            '(' + \
            ', '.join([str(param) for param in self.params]) + \
            ') -> ' + \
            self.returns
