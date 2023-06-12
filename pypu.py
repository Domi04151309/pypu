#!/usr/bin/env python3
"""
.. include:: ./example.svg
"""

import argparse
import os
import sys

import requests

from data.SourceFile import SourceFile
from data.UMLFile import UMLFile
from utils.ModuleParser import get_module_info
from utils.PlantEncoder import encode


def generate_uml(directory: str) -> str:
    """
    Generates a valid PlantUML string for all files in the given directory and its subdirectories.

    :param directory: The directory to process.
    :return: A valid PlantUML string.
    """
    known_modules: list[str] = []
    source_files: list[SourceFile] = []
    blacklist: list[str] = ['venv', '/.', '__']
    for root, _, files in os.walk(directory):
        for file in files:
            if '.py' in file:
                file_path: str = os.path.join(root, file.split('.')[0])
                if not any(item in file_path for item in blacklist):
                    known_modules.append('.'.join([
                        x for x in file_path[len(directory):].split(os.sep) if x
                    ]))

    for root, _, files in os.walk(directory):
        for file in files:
            if '.py' in file:
                file_path = os.path.join(root, file)
                if not any(item in file_path for item in blacklist):
                    source_files.append(
                        get_module_info(directory, file_path, known_modules)
                    )
    return str(UMLFile(source_files))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--module', help='the module to analyze', required=True)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-l', '--link', help='returns a link to the diagram in the specified format')
    group.add_argument('-f', '--format', help='returns the diagram in the specified format')
    args = parser.parse_args()

    uml: str = generate_uml(args.module)
    if args.link:
        print(encode(uml, args.link))
    elif args.format:
        result = requests.get(encode(uml, args.format), timeout=3, allow_redirects=False)
        if result.status_code == 200:
            sys.stdout.buffer.write(result.content)
    else:
        print(uml)
