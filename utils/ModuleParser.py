import os
import astroid
from astroid import NodeNG, FunctionDef

from data.SourceFile import SourceFile
from data.SourceClass import SourceClass
from data.SourceFunction import SourceFunction
from data.SourceVariable import SourceVariable


def annotation_to_string(node: NodeNG | None, string: str = '') -> str:
    """
    Generates a type string from annotation nodes.

    :param node: The root annotation node.
    :param string: The parent string identifier for recursive parsing.
    :return: A human-readable type string.
    """
    return_value = ''
    if isinstance(node, astroid.Name):
        return_value = node.name
    elif isinstance(node, astroid.Subscript) and isinstance(node.value, astroid.Name):
        if isinstance(node.slice, astroid.Tuple):
            return_value = node.value.name + \
                           '[' + \
                           ', '.join([annotation_to_string(child_node) for child_node in
                                      node.slice.elts]) + \
                           ']'
        elif isinstance(node.slice, astroid.Attribute):
            return_value = annotation_to_string(node.slice, node.value.name)
    elif isinstance(node, astroid.Attribute):
        return_value = node.attrname
    elif isinstance(node, astroid.Const):
        return_value = str(node.value)
    elif isinstance(node, astroid.BinOp):
        return_value = annotation_to_string(node.left) + ' | ' + annotation_to_string(node.right)
    return (string + '[' if string else '') + return_value + (']' if string else '')


def get_function(node: FunctionDef) -> SourceFunction:
    """
    Generates a source function based on the input node.

    :param node: The input node.
    :return: A source function.
    """
    function: SourceFunction = SourceFunction()
    function.name = node.name
    function.returns = annotation_to_string(node.returns)
    if node.decorators is not None:
        for decorator in node.decorators.nodes:
            if isinstance(decorator, astroid.Name) and \
                    decorator.name == 'staticmethod':
                function.static = True
    for i, arg in enumerate(node.args.args):
        function.params.append(
            SourceVariable(
                arg.name,
                annotation_to_string(
                    node.args.annotations[i]
                )
            )
        )
    return function


def get_module_info(
        file_path: str,
        known_modules: list[str],
        with_dependencies: bool = False
) -> SourceFile:
    """
    Generates a source file based on the provided file path.

    :param file_path: The file path for which to generate the source file.
    :param known_modules: All known local modules.
    :param with_dependencies: Whether external dependencies should be included.
    :return: A matching source file.
    """
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
                    if isinstance(child_node, FunctionDef):
                        new_class.methods.append(get_function(child_node))
                        for child_child_node in child_node.body:
                            if isinstance(child_child_node, astroid.AnnAssign) and \
                                    isinstance(child_child_node.target, astroid.AssignAttr):
                                print(child_child_node.target)
                                new_class.variables.append(
                                    SourceVariable(
                                        child_child_node.target.attrname,
                                        annotation_to_string(child_child_node.annotation)
                                    )
                                )
                    elif isinstance(child_node, astroid.AnnAssign) and \
                            isinstance(child_node.target, astroid.AssignName):
                        new_class.variables.append(
                            SourceVariable(
                                child_node.target.name,
                                annotation_to_string(child_node.annotation)
                            )
                        )
                source_file.classes.append(new_class)
            elif isinstance(node, FunctionDef):
                source_file.functions.append(get_function(node))
            elif isinstance(node, astroid.AnnAssign) and \
                    isinstance(node.target, astroid.AssignName):
                source_file.variables.append(
                    SourceVariable(node.target.name, annotation_to_string(node.annotation))
                )
            elif isinstance(node, astroid.Import):
                if with_dependencies:
                    for node_name in node.names:
                        source_file.imports.append(node_name[0])
            elif isinstance(node, astroid.ImportFrom):
                if node.level == 1 or node.modname in known_modules or with_dependencies:
                    for node_name in node.names:
                        source_file.imports.append(
                            ('.'.join(path_modules[:-1]) + '.' if node.level == 1 else '') +
                            node.modname + '.' + node_name[0]
                        )
        return source_file
    except astroid.AstroidBuildingException:
        return SourceFile()
