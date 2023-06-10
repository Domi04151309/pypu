from utils.SourceClass import SourceClass
from utils.SourceFunction import SourceFunction


class SourceFile:
    def __init__(self) -> None:
        self.name: str = ''
        self.imports: list[str] = []
        self.functions: list[SourceFunction] = []
        self.classes: list[SourceClass] = []
