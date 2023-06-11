class SourceType:
    """
    Data class representing a python type.
    """

    def __init__(self, readable: str = 'Any', dependencies: set[str] | None = None) -> None:
        self.readable: str = readable
        self.dependencies: set[str] = {'Any'} if dependencies is None else dependencies

    def __str__(self) -> str:
        return self.readable
