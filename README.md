# PyPu

PyPu is a lightweight Python script designed to facilitate the generation of PlantUML 
diagrams from Python source code.

## How to run

To run this program, you have to install `python` and `pip` first.
The following guides will help you install it.

- [python](https://wiki.python.org/moin/BeginnersGuide/Download)
- [pip](https://pip.pypa.io/en/stable/installation/)

After installing `python` and `pip`, you can now install the dependencies.
Use the following command to do so.

```bash
python3 -m pip install -U -r requirements.txt
```

Now that the dependencies are installed, simply run the following command. Replace `.`
with the folder that you want to index and `output.puml` with the desired output location.

```bash
./pypu.py --module . > output.puml
```

You can add an optional additional parameter to get a link to a rendered file.

```bash
./pypu.py -m . --link svg
```

Alternatively, you can add an optional additional parameter to get the rendered file directly.

```bash
./pypu.py -m . --format svg > output.svg
```

## Development

### Documentation

To access the automatically generated documentation, please utilize the
following command.

```bash
pdoc pypu.py utils data --favicon https://fonts.gstatic.com/s/i/short-term/release/materialsymbolsoutlined/code/default/48px.svg --logo https://fonts.gstatic.com/s/i/short-term/release/materialsymbolsoutlined/code/default/48px.svg
```

### Class Diagrams

![Diagram](example.svg?raw=true)

## Linting

Linting is an essential step in ensuring code quality and maintainability. For
this project, we are using Pylint, a widely-used linter that can identify
potential issues in the code.

To lint the entire repository, simply use the following command in a terminal:

```bash
pylint --recursive yes --ignore="__pycache__,venv,.mypy_cache" --output-format=colorized .
```

This command will recursively search through all subdirectories of the current
directory and analyze all Python files while ignoring any files or directories
whose names match the given regular expression.

## Type Checking

By running the following command, MyPy will perform static type checking on the
project files. MyPy analyzes the code and provides feedback on type
inconsistencies, potential type errors, and other type-related issues.

```bash
mypy pypu.py --strict
```

Static type checking helps catch errors and improve code quality by ensuring
that variables, function arguments, and return types are used consistently and
correctly according to their declared types. MyPy verifies type annotations and
provides warnings or errors if it finds any inconsistencies or violations.