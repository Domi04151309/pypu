def var_test(file_path):
    with open(file_path, 'r') as file:
        lines: list[str] = []
        line: str = ''
        multi_line_single_counter: int = 0
        multi_line_double_counter: int = 0
        bracket_counter: int = 0
        is_in_multi_line_string: bool = False
        is_in_comment: bool = False
        while 1:
            #TODO: detect single-line strings

            # Read next character
            char = file.read(1)
            if not char:
                break

            # Detect multi-line strings
            if char == '"':
                multi_line_double_counter += 1
            else:
                multi_line_double_counter = 0
            if char == "'":
                multi_line_single_counter += 1
            else:
                multi_line_single_counter = 0
            if multi_line_single_counter == 3 or multi_line_double_counter == 3:
                is_in_multi_line_string = not is_in_multi_line_string
            if is_in_multi_line_string:
                continue

            # Detect comments
            if char == '#':
                is_in_comment = True
            elif char == '\n':
                is_in_comment = False
            if is_in_comment:
                continue

            # Detect brackets
            if char == '(':
                bracket_counter += 1
            elif char == ')':
                bracket_counter -= 1
                continue
            if bracket_counter > 0:
                continue

            # Save the line
            if char == '\n':
                lines.append(line)
                line = ''
            else:
                line += char

        print(file_path)
        class_indent = []
        function_indent = 0
        variables: list[str] = []
        for line in lines:
            # Empty line detection
            if len(line) == 0:
                continue

            # Function detection
            if function_indent > 0 and \
                    len(line) - len(line.lstrip(' ')) <= function_indent and \
                    not line.strip().startswith(')'):
                function_indent = 0
            if function_indent == 0 and 'def ' in line:
                function_indent = len(line) - len(line.lstrip(' '))

            # Class Detection
            if len(class_indent) > 0 and len(line) - len(line.lstrip(' ')) <= class_indent[-1][1] and \
                    not line.strip().startswith(')'):
                class_indent.pop()
            if 'class ' in line:
                class_indent.append((find_between(line, 'class ', ':'), len(line) - len(line.lstrip(' '))))

            # Relevant line detection
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
                            variable_string = part_variable.strip()
                            if len(class_indent) > 0:
                                variable_string = variable_string.replace('self.', class_indent[-1][0] + '.')
                            variables.append(variable_string)
                    else:
                        variable_string = variable_definition.strip()
                        if len(class_indent) > 0:
                            variable_string = variable_string.replace('self.', class_indent[-1][0] + '.')
                        variables.append(variable_string)
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


def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""
