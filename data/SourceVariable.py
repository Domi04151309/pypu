class SourceVariable:
    """
    Data class representing a python variable.
    """

    def __init__(self, name: str, data_type: str, static: bool = False) -> None:
        self.static = static
        self.name: str = name
        self.type: str = data_type

    def __str__(self) -> str:
        return ('{static}' if self.static else '') + \
            self.name + \
            (': <color:MidnightBlue>' + self.type + '</color>' if self.type else '')
