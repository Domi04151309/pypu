import os
import astroid

from utils.SourceFile import SourceFile
from utils.SourceClass import SourceClass
from utils.SourceFunction import SourceFunction


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
                        new_function.name = node.name
                        for arg in child_node.args.args:
                            new_function.params.append(arg.name)
                        new_class.methods.append(new_function)
                source_file.classes.append(new_class)
            elif isinstance(node, astroid.FunctionDef):
                new_function: SourceFunction = SourceFunction()
                new_function.name = node.name
                for arg in node.args.args:
                    new_function.params.append(arg.name)
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


def print_module_info(source_file):
    print('package ' + source_file.name + ' {')
    if source_file.functions:
        print('  object ' + source_file.name + 'Companion {')
        for function in source_file.functions:
            print('    ' + function.name + '(' + ', '.join(function.params) + ')')
        print('  }')
    for source_class in source_file.classes:
        print('  class ' + source_class.name + ' {')
        if source_class.methods:
            for function in source_class.methods:
                print('    ' + function.name + '(' + ', '.join(function.params) + ')')
        print('  }')
    print('}')
    for source_import in source_file.imports:
        print(source_file.name + ' ..> ' + source_import)


def generate_uml(directory):
    print('@startuml')
    for root, dirs, files in os.walk(directory):
        for file in files:
            if '.py' in file:
                file_path = os.path.join(root, file)
                if '__' not in file_path:
                    info = get_module_info(file_path)
                    print_module_info(info)
    print('@enduml')


# Provide the directory path for listing files recursively
directory_path = '../Stator_Analyzer/utils'
generate_uml(directory_path)
