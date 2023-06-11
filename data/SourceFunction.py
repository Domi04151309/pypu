from data.SourceType import SourceType
from data.SourceVariable import SourceVariable


class SourceFunction:
    """
    Data class representing a python function.
    """

    def __init__(self) -> None:
        self.static = False
        self.name: str = ''
        self.params: list[SourceVariable] = []
        self.returns: SourceType = SourceType()

    def get_dependencies(self) -> set[str]:
        """
        Generates a list of dependencies.

        :return: All dependencies of the function.
        """
        return self.returns.dependencies.union(
            {inner for outer in self.params for inner in outer.get_dependencies()}
        )

    def __str__(self) -> str:
        return ('{static}' if self.static else '') + \
            '<color:DarkRed>' + \
            self.name + \
            '</color>(' + \
            ', '.join([str(param) for param in self.params]) + \
            ')' + \
            (
                ' → <color:MidnightBlue>' + str(self.returns) + '</color>'
                if str(self.returns) else ''
            )
