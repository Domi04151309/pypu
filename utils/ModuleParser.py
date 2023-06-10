import os
import astroid

from data.SourceFile import SourceFile
from data.SourceClass import SourceClass
from data.SourceFunction import SourceFunction
from data.SourceVariable import SourceVariable


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
        path_modules = file_path.split('.')[-2].split(os.sep)
        source_file = SourceFile()
        source_file.name = '.'.join(path_modules)

        for node in module.body:
            if isinstance(node, astroid.ClassDef):
                new_class: SourceClass = SourceClass()
                new_class.name = node.name
                for child_node in node.body:
                    if isinstance(child_node, astroid.FunctionDef):
                        new_function: SourceFunction = SourceFunction()
                        new_function.name = child_node.name
                        new_function.returns = annotation_to_string(child_node.returns)
                        if child_node.decorators is not None:
                            for decorator in child_node.decorators.nodes:
                                if isinstance(decorator, astroid.Name) and decorator.name == 'staticmethod':
                                    new_function.static = True
                        for i, arg in enumerate(child_node.args.args):
                            new_function.params.append(
                                SourceVariable(arg.name, annotation_to_string(child_node.args.annotations[i]))
                            )
                        new_class.methods.append(new_function)
                source_file.classes.append(new_class)
            elif isinstance(node, astroid.FunctionDef):
                new_function: SourceFunction = SourceFunction()
                new_function.name = node.name
                new_function.returns = annotation_to_string(node.returns)
                for i, arg in enumerate(node.args.args):
                    new_function.params.append(SourceVariable(arg.name, annotation_to_string(node.args.annotations[i])))
                source_file.functions.append(new_function)
            elif isinstance(node, astroid.Import):
                if with_dependencies:
                    for node_name in node.names:
                        source_file.imports.append(node_name[0])
            elif isinstance(node, astroid.ImportFrom):
                if node.level == 1 or with_dependencies:
                    for node_name in node.names:
                        source_file.imports.append(
                            '.'.join(path_modules[:-1]) + '.' + node.modname + '.' + node_name[0]
                        )
        return source_file
    except astroid.AstroidBuildingException:
        return SourceFile()
