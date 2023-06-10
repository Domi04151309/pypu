import os

from data.SourceFile import SourceFile
from data.UMLFile import UMLFile
from utils.ModuleParser import get_module_info
from utils.VariableParser import add_variable_information


def generate_uml(directory):
    source_files: list[SourceFile] = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if '.py' in file:
                file_path: str = os.path.join(root, file)
                if '__' not in file_path:
                    source_files.append(add_variable_information(file_path, get_module_info(file_path)))
    print(UMLFile(source_files))


# Provide the directory path for listing files recursively
directory_path = '../Stator_Analyzer/utils'
generate_uml(directory_path)
