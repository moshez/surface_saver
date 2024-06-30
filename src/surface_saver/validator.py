import json
from jsonschema import validate
from jsonschema.exceptions import ValidationError
import importlib.resources
import pathlib
from typing import Dict, List, Tuple, Generator, Any

import surface_saver


class InvalidFileError(Exception):
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
    items: List[Dict[str, Any]] = json.loads(root_json.read_text())
    schema: Dict[str, Any] = json.loads(_SCHEMA_PATH.read_text())
    parent: pathlib.Path = root_json.parent
    for an_item in items:
        name: str = an_item["name"].replace(" ", "-").lower()
        directory: pathlib.Path = parent / name
        if not directory.exists():
            continue
        for child in directory.glob("*.json"):
            print("Checking", child)
            try:
                _validate_json_file(child, schema)
            except InvalidFileError as exc:
                yield child, exc
