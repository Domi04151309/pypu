from data.SourceVariable import SourceVariable


class SourceFunction:
    def __init__(self) -> None:
        self.name: str = ''
        self.params: list[SourceVariable] = []
        self.returns: str = 'Any'

    def __str__(self) -> str:
        return self.name + \
            '(' + \
            ', '.join([str(param) for param in self.params]) + \
            ') -> ' + \
            self.returns
