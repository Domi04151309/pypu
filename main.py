import os
import astroid


def get_module_info(file_path):
    try:
        module = astroid.MANAGER.ast_from_file(file_path)
        classes = {}
        global_functions = []

        for node in module.body:
            if isinstance(node, astroid.ClassDef):
                class_name = node.name
                class_functions = []

                for child_node in node.body:
                    if isinstance(child_node, astroid.FunctionDef):
                        function_name = child_node.name
                        args = []

                        for arg in child_node.args.args:
                            args.append(arg.name)

                        class_functions.append((function_name, args))

                classes[class_name] = class_functions
            elif isinstance(node, astroid.FunctionDef):
                function_name = node.name
                args = []

                for arg in node.args.args:
                    args.append(arg.name)

                global_functions.append((function_name, args))
            elif isinstance(node, astroid.Import):
                for node_name in node.names:
                    print('Dummy --> ' + node_name[0])
            elif isinstance(node, astroid.ImportFrom):
                for node_name in node.names:
                    print('Dummy --> ' + node.modname + '.' + node_name[0])

        file_name_parts = file_path.split('.')[1].split(os.sep)
        print(f"package {'.'.join(file_name_parts)} {'{'}")
        if global_functions:
            print(f"  object {file_name_parts[-1]}Companion {'{'}")
            for function_name, args in global_functions:
                print(f"    {function_name}({', '.join(args)})")
            print("  }")
        for class_name, functions in classes.items():
            print(f"  class {class_name} {'{'}")
            if functions:
                for function_name, args in functions:
                    print(f"    {function_name}({', '.join(args)})")
            print("  }")
        print("}")

    except astroid.AstroidBuildingException:
        print(f"Failed to import module: {file_path}")

def list_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if '.py' in file:
                file_path = os.path.join(root, file)
                if '__' not in file_path:
                    get_module_info(file_path)


# Provide the directory path for listing files recursively
directory_path = "../Stator_Analyzer/utils"

print("@startuml")
list_files(directory_path)
print("@enduml")
