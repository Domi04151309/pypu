import os
import astroid

from utils.SourceFile import SourceFile
from utils.SourceClass import SourceClass
from utils.SourceFunction import SourceFunction
from utils.UMLFile import UMLFile
from utils.VariableParser import var_test


def annotation_to_string(node) -> str:
    if isinstance(node, astroid.Name):
        return node.name
    elif isinstance(node, astroid.Subscript):
        return node.value.name
    elif isinstance(node, astroid.Const):
        return str(node.value)
    return 'Any'


def get_module_info(file_path, with_dependencies: bool = False):
    try:
        module = astroid.MANAGER.ast_from_file(file_path)
        source_file = SourceFile()
        source_file.name = file_path.split('.')[-2].split(os.sep)[-1]

        for node in module.body:
            if isinstance(node, astroid.ClassDef):
                new_class: SourceClass = SourceClass()
                new_class.name = node.name
                for child_node in node.body:
                    if isinstance(child_node, astroid.FunctionDef):
                        new_function: SourceFunction = SourceFunction()
                        new_function.name = child_node.name
                        new_function.returns = annotation_to_string(child_node.returns)
                        for i, arg in enumerate(child_node.args.args):
                            new_function.params.append((arg.name, annotation_to_string(child_node.args.annotations[i])))
                        new_class.methods.append(new_function)
                source_file.classes.append(new_class)
            elif isinstance(node, astroid.FunctionDef):
                new_function: SourceFunction = SourceFunction()
                new_function.name = node.name
                new_function.returns = annotation_to_string(node.returns)
                for i, arg in enumerate(node.args.args):
                    new_function.params.append((arg.name, annotation_to_string(node.args.annotations[i])))
                source_file.functions.append(new_function)
            elif isinstance(node, astroid.Import):
                if with_dependencies:
                    for node_name in node.names:
                        source_file.imports.append(node_name[0])
            elif isinstance(node, astroid.ImportFrom):
                if node.level == 1 or with_dependencies:
                    for node_name in node.names:
                        source_file.imports.append(node.modname + '.' + node_name[0])
        return source_file
    except astroid.AstroidBuildingException:
        return SourceFile()


def generate_uml(directory):
    source_files: list[SourceFile] = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if '.py' in file:
                file_path: str = os.path.join(root, file)
                if '__' not in file_path:
                    source_files.append(get_module_info(file_path))
                    var_test(file_path)
    #print(UMLFile(source_files))


# Provide the directory path for listing files recursively
directory_path = '../Stator_Analyzer/utils'
generate_uml(directory_path)
