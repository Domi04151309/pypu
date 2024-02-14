#!/usr/bin/env python3
"""
.. include:: ./example.svg
"""

import argparse
import os
import sys
from argparse import _MutuallyExclusiveGroup

import astroid
import requests

from data.SourceFile import SourceFile
from data.UMLFile import UMLFile
from utils.ModuleParser import get_module_info
from utils.PlantEncoder import encode


def get_known_modules(directory: str, blacklist: list[str]) -> list[str]:
    """
    Gets a `list` of all modules in a directory and its subdirectories.

    :param directory: The directory to process.
    :param blacklist: A `list` of forbidden substrings.
    :return: A `list` of known modules.
    """
    known_modules: list[str] = []
    for root, _, files in os.walk(directory):
        for file in files:
            if '.py' in file:
                file_path: str = os.path.join(root, file.split('.')[0])
                if not any(item in file_path for item in blacklist):
                    known_modules.append('.'.join([
                        x for x in file_path[len(directory):].split(os.sep) if x
                    ]))
    return known_modules


def get_source_files(
        directory: str,
        known_modules: list[str],
        blacklist: list[str]
) -> list[SourceFile]:
    """
    Gets a `list` of all source files in a directory and its subdirectories.

    :param directory: The directory to process.
    :param known_modules: A `list` of known modules.
    :param blacklist: A `list` of forbidden substrings.
    :return: A `list` of source files.
    """
    source_files: list[SourceFile] = []
    for root, _, files in os.walk(directory):
        for file in files:
            if '.py' in file:
                file_path = os.path.join(root, file)
                if not any(item in file_path for item in blacklist):
                    try:
                        source_files.append(
                            get_module_info(directory, file_path, known_modules)
                        )
                    except astroid.AstroidBuildingException:
                        pass
    return source_files


def generate_uml(directory: str) -> str:
    """
    Generates a valid PlantUML string for all files in the given directory and its subdirectories.

    :param directory: The directory to process.
    :return: A valid PlantUML string.
    """
    blacklist: list[str] = ['venv', '/.', '__']
    known_modules: list[str] = get_known_modules(directory, blacklist)
    source_files: list[SourceFile] = get_source_files(directory, known_modules, blacklist)
    return str(UMLFile(source_files))


if __name__ == '__main__':
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('-m', '--module', help='the module to analyze', required=True)
    group: _MutuallyExclusiveGroup = parser.add_mutually_exclusive_group()
    group.add_argument('-l', '--link', help='returns a link to the diagram in the specified format')
    group.add_argument('-f', '--format', help='returns the diagram in the specified format')
    args: argparse.Namespace = parser.parse_args()

    uml: str = generate_uml(args.module)
    if args.link:
        print(encode(uml, args.link))
    elif args.format:
        encoded: str = encode(uml, args.format)
        result: requests.Response | None = None
        try:
            result = requests.get(encoded, timeout=3, allow_redirects=False)
        except requests.ReadTimeout:
            print(
                'The rendering server took too long to respond. Try visiting "' +
                encoded +
                '" in a browser.'
            )
        if result is not None and result.status_code == 200:
            sys.stdout.buffer.write(result.content)
    else:
        print(uml)
