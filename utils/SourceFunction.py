class SourceFunction:
    def __init__(self) -> None:
        self.name: str = ''
        self.params: list[tuple[str, str]] = []
        self.returns: str = 'Any'

    def __str__(self) -> str:
        return self.name + \
            '(' + \
            ', '.join([param[0] + ': ' + param[1] for param in self.params]) + \
            ') -> ' + \
            self.returns
