from data.SourceFile import SourceFile


class UMLFile:
    def __init__(self, source_files: list[SourceFile]) -> None:
        self.source_files: list[SourceFile] = source_files

    def __str__(self) -> str:
        file: str = '@startuml\n' + \
            'skinparam packageStyle frame\n' + \
            'hide empty members\n' + \
            '\n'.join([str(source_file) for source_file in self.source_files]) + \
            '\n' + \
            '\n'.join([source_file.get_connection_strings() for source_file in self.source_files]) + \
            '\n@enduml'
        return '\n'.join([line for line in file.split('\n') if line.strip()])
