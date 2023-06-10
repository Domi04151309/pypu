from data.SourceVariable import SourceVariable


class SourceFunction:
    """
    Data class representing a python function.
    """

    def __init__(self) -> None:
        self.static = False
        self.name: str = ''
        self.params: list[SourceVariable] = []
        self.returns: str = 'Any'

    def __str__(self) -> str:
        return ('{static}' if self.static else '') + \
            '<color:DarkRed>' + \
            self.name + \
            '</color>(' + \
            ', '.join([str(param) for param in self.params]) + \
            ')' + (' → <color:MidnightBlue>' + self.returns + '</color>' if self.returns else '')
