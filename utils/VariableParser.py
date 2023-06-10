def var_test(file_path):
    with open(file_path, 'r') as file:
        lines: list[str] = []
        line: str = ''
        comment_single_counter: int = 0
        comment_double_counter: int = 0
        bracket_counter: int = 0
        is_in_multi_line_string: bool = False
        is_in_comment: bool = False
        while 1:
            #TODO: detect single strings
            char = file.read(1)
            if not char:
                break

            if char == '"':
                comment_double_counter += 1
            else:
                comment_double_counter = 0
            if char == "'":
                comment_single_counter += 1
            else:
                comment_single_counter = 0
            if comment_single_counter == 3 or comment_double_counter == 3:
                is_in_multi_line_string = not is_in_multi_line_string
            if is_in_multi_line_string:
                continue

            if char == '#':
                is_in_comment = True
            elif char == '\n':
                is_in_comment = False
            if is_in_comment:
                continue

            if char == '(':
                bracket_counter += 1
            elif char == ')':
                bracket_counter -= 1
                continue
            if bracket_counter > 0:
                continue

            if char == '\n':
                lines.append(line)
                line = ''
            else:
                line += char

        print(file_path)
        function_indent = 0
        variables: list[str] = []
        for line in lines:
            #TODO: detect classes
            if len(line) == 0:
                continue
            if function_indent > 0 and \
                    len(line) - len(line.lstrip(' ')) <= function_indent and \
                    not line.strip().startswith(')'):
                function_indent = 0
            if function_indent == 0 and 'def ' in line:
                function_indent = len(line) - len(line.lstrip(' '))

            variable_definition = line.strip().split('=')[0]
            if '=' in line and (function_indent == 0 or (function_indent > 0 and 'self.' in variable_definition)):
                if 'if ' not in variable_definition and \
                        '[' not in variable_definition and \
                        '+' not in variable_definition and \
                        '-' not in variable_definition and \
                        '*' not in variable_definition and \
                        '/' not in variable_definition and \
                        ('.' not in variable_definition or 'self.' in variable_definition):
                    if ',' in variable_definition:
                        for part_variable in variable_definition.split(','):
                            variables.append(part_variable.strip())
                    else:
                        variables.append(variable_definition.strip())
        variables.sort()
        variables_with_types = {}
        for var in variables:
            split_var = var.split(':')
            if len(split_var) == 2:
                variables_with_types[split_var[0].strip()] = split_var[1].strip()
            elif split_var[0] not in variables_with_types:
                variables_with_types[split_var[0].strip()] = 'Any'
        for key, value in variables_with_types.items():
            print('    ' + key + ': ' + value)