from .SourceFile import SourceFile


class UMLFile:
    """
    Data class representing a PlantUML file.
    """

    def __init__(self, source_files: list[SourceFile]) -> None:
        self.source_files: list[SourceFile] = source_files

    def get_known_modules(self) -> list[str]:
        """
        Generates a list of valid modules.

        :return: A list of valid modules
        """
        packages = []
        for file in self.source_files:
            # noinspection PyTypeChecker
            for item in file.variables + file.functions + file.classes:
                packages.append(file.name + '.' + item.name)
        return packages

    def __str__(self) -> str:
        file: str = '@startuml\n' + \
            'left to right direction\n' + \
            'skinparam packageStyle frame\n' + \
            'skinparam packageBorderColor gray\n' + \
            'skinparam classBackgroundColor white\n' + \
            'skinparam objectBackgroundColor white\n' + \
            'hide empty members\n' + \
            'hide circle\n' + \
            '\n'.join([
                str(source_file)
                for source_file in self.source_files
            ]) + \
            '\n' + \
            '\n'.join([
                source_file.get_connection_strings(self.get_known_modules())
                for source_file in self.source_files
            ]) + \
            '\n@enduml'
        return '\n'.join([line for line in file.split('\n') if line.strip()])
