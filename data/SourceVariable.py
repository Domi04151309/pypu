class SourceVariable:
    def __init__(self, name: str, data_type: str) -> None:
        self.name: str = name
        self.type: str = data_type

    def __str__(self) -> str:
        return self.name + \
            (': ' + self.type if self.type else '')
