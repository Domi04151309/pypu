import os
import astroid
from astroid import NodeNG, FunctionDef

from data.SourceFile import SourceFile
from data.SourceClass import SourceClass
from data.SourceFunction import SourceFunction
from data.SourceType import SourceType
from data.SourceVariable import SourceVariable


def annotation_to_string(node: NodeNG | None) -> SourceType:
    """
    Generates a type string from annotation nodes.

    :param node: The root annotation node.
    :return: A human-readable type string.
    """
    string_annotation: str = ''
    type_set: set[str] = set()
    if isinstance(node, astroid.Name):
        string_annotation = node.name
        type_set.add(node.name)
    elif isinstance(node, astroid.Subscript) and isinstance(node.value, astroid.Name):
        if isinstance(node.slice, astroid.Tuple):
            string_annotation = node.value.name + '['
            for child_node in node.slice.elts:
                inner_annotation = annotation_to_string(child_node)
                string_annotation += str(inner_annotation) + ', '
                type_set.update(inner_annotation.dependencies)
            string_annotation = string_annotation[:-2]
            string_annotation += ']'
        elif isinstance(node.slice, astroid.Attribute) or isinstance(node.slice, astroid.Name):
            inner_annotation = annotation_to_string(node.slice)
            string_annotation = node.value.name + '[' + str(inner_annotation) + ']'
            type_set.update(inner_annotation.dependencies)
    elif isinstance(node, astroid.Attribute):
        string_annotation = node.attrname
        type_set.add(node.attrname)
    elif isinstance(node, astroid.Const):
        string_annotation = str(node.value)
        type_set.add(str(node.value))
    elif isinstance(node, astroid.BinOp):
        left = annotation_to_string(node.left)
        right = annotation_to_string(node.right)
        string_annotation = str(left) + ' | ' + str(right)
        type_set.update(left.dependencies)
        type_set.update(right.dependencies)
    return SourceType(string_annotation, type_set)


def get_function(node: FunctionDef) -> SourceFunction:
    """
    Generates a source function based on the input node.

    :param node: The input node.
    :return: A source function.
    """
    annotation = annotation_to_string(node.returns)
    function: SourceFunction = SourceFunction()
    function.name = node.name
    function.returns = annotation
    if node.decorators is not None:
        for decorator in node.decorators.nodes:
            if isinstance(decorator, astroid.Name) and \
                    decorator.name == 'staticmethod':
                function.static = True
    for i, arg in enumerate(node.args.args):
        annotation = annotation_to_string(node.args.annotations[i])
        function.params.append(
            SourceVariable(
                arg.name,
                annotation
            )
        )
    return function


def get_module_info(
        root: str,
        file_path: str,
        known_modules: list[str],
        with_dependencies: bool = False
) -> SourceFile:
    """
    Generates a source file based on the provided file path.

    :param root: The root path of the analysis.
    :param file_path: The file path for which to generate the source file.
    :param known_modules: All known local modules.
    :param with_dependencies: Whether external dependencies should be included.
    :return: A matching source file.
    """
    try:
        module = astroid.MANAGER.ast_from_file(file_path)
        path_modules = file_path[len(root):].split('.')[-2].split(os.sep)
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
                                annotation_to_string(child_node.annotation),
                                True
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
