import argparse
import json
import importlib.resources
import pathlib
from typing import Dict, List, Tuple, Generator, Any

from gather.commands import add_argument
from . import ENTRY_DATA
from jsonschema import validate
from jsonschema.exceptions import ValidationError

import surface_saver


class InvalidFileError(Exception):
    """
    Custom exception for invalid JSON files.

    Args:
        original_exception (Exception): The original exception that was raised.
        file_path (pathlib.Path): The path to the file that caused the error.

    Attributes:
        original_exception (Exception): The original exception that was raised.
        file_path (pathlib.Path): The path to the file that caused the error.
    """

    def __init__(self, original_exception: Exception, file_path: pathlib.Path):
        self.original_exception = original_exception
        self.file_path = file_path
        super().__init__(f"Error in file {file_path}: {original_exception}")


def _validate_json_file(file_path: pathlib.Path, schema: Dict[str, Any]) -> None:
    try:
        contents = file_path.read_text()
        data = json.loads(contents)
        validate(instance=data, schema=schema)
    except (IOError, json.JSONDecodeError, ValidationError) as exc:
        raise InvalidFileError(exc, file_path)


_SCHEMA_PATH = importlib.resources.files(surface_saver) / "box-contents-schema.json"


def validate_all_json_files(
    root_json: pathlib.Path,
) -> Generator[Tuple[pathlib.Path, InvalidFileError], None, None]:
    """
    Validate all JSON files in the directory structure defined by the root JSON file.

    This function reads the root JSON file,
    which should contain a list of items with 'name' fields.
    It then looks for directories named after these items
    (with spaces replaced by hyphens and lowercased)
    and validates all JSON files within these directories against the schema.

    Args:
        root_json (pathlib.Path): The path to the root JSON file.

    Yields:
        Tuple[pathlib.Path, InvalidFileError]: A tuple containing the path of an
        invalid JSON file and the corresponding InvalidFileError exception.
    """
    items: List[Dict[str, Any]] = json.loads(root_json.read_text())
    schema: Dict[str, Any] = json.loads(_SCHEMA_PATH.read_text())
    parent: pathlib.Path = root_json.parent
    for an_item in items:
        name: str = an_item["name"].replace(" ", "-").lower()
        directory: pathlib.Path = parent / name
        if not directory.exists():
            continue
        for child in directory.glob("*.json"):
            try:
                _validate_json_file(child, schema)
            except InvalidFileError as exc:
                yield child, exc


@ENTRY_DATA.register(add_argument("json_directory"), name="validate")
def _validate(args: argparse.Namespace) -> None:  # pragma: no cover
    for fpath, exc in validate_all_json_files(pathlib.Path(args.json_directory)):
        print(f"Invalid file: {fpath}: {exc}")
