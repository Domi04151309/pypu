from .SourceType import SourceType


class SourceVariable:
    """
    Data class representing a python variable.
    """

    def __init__(self, name: str, data_type: SourceType, static: bool = False) -> None:
        self.static: bool = static
        self.name: str = name
        self.type: SourceType = data_type

    def get_dependencies(self) -> set[str]:
        """
        Generates a list of dependencies.

        :return: All dependencies of the variable.
        """
        return self.type.dependencies

    def __str__(self) -> str:
        return ('{static}' if self.static else '') + \
            self.name + \
            (': <color:MidnightBlue>' + str(self.type) + '</color>' if str(self.type) else '')
