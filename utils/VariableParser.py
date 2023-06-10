def prefilter_file(file_path: str) -> list[str]:
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
        return lines


def get_variables(lines: list[str]) -> list[tuple[str, str]]:
    class_indents = []
    function_indent = 0
    variables_with_types = {}
    for line in lines:
        # Detect irrelevant lines
        if len(line) == 0 or not any(keyword in line for keyword in ['class ', 'def ', '=']):
            continue

        # Detect classes
        if len(class_indents) > 0 and len(line) - len(line.lstrip(' ')) <= class_indents[-1][1] and \
                not line.strip().startswith(')'):
            class_indents.pop()
        if 'class ' in line:
            class_indents.append((find_between(line, 'class ', ':'), len(line) - len(line.lstrip(' '))))

        # Detect functions
        if function_indent > 0 and \
                len(line) - len(line.lstrip(' ')) <= function_indent and \
                not line.strip().startswith(')'):
            function_indent = 0
        if function_indent == 0 and 'def ' in line:
            function_indent = len(line) - len(line.lstrip(' '))

        # Filter relevant assignments
        definition_part = line.strip().split('=')[0]
        if '=' in line and (function_indent == 0 or (function_indent > 0 and 'self.' in definition_part)):
            if 'if ' not in definition_part and \
                    '[' not in definition_part and \
                    '+' not in definition_part and \
                    '-' not in definition_part and \
                    '*' not in definition_part and \
                    '/' not in definition_part and \
                    ('.' not in definition_part or 'self.' in definition_part):
                if ',' in definition_part:
                    variable_definitions = definition_part.split(',')
                else:
                    variable_definitions = [definition_part]
                for variable in variable_definitions:
                    variable_string = variable.strip()
                    if len(class_indents) > 0:
                        variable_string = variable_string.replace('self.', class_indents[-1][0] + '.')
                    split_var = variable_string.split(':')
                    if len(split_var) == 2:
                        variables_with_types[split_var[0].strip()] = split_var[1].strip()
                    elif split_var[0] not in variables_with_types:
                        variables_with_types[split_var[0].strip()] = 'Any'
    return list(variables_with_types.items())


def var_test(file_path):
    lines = prefilter_file(file_path)
    variables = get_variables(lines)
    print(file_path)
    for key, value in variables:
        print('    ' + key + ': ' + value)


def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""
