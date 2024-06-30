import json
import os
from jsonschema import validate
from jsonschema.exceptions import ValidationError
import importlib.resources
import pathlib

import surface_saver

class InvalidFileError(Exception):
    pass

def _validate_json_file(file_path, schema):
    try:
        contents = file_path.read_text()
        data = json.loads(contents)
        validate(instance=data, schema=schema)
    except (IOError, json.JSONDecodeError, ValidationError) as exc:
        raise InvalidFileError(exc, file_path)

_SCHEMA_PATH = importlib.resources.files(surface_saver) / "box-contents-schema.json"

def validate_all_json_files(root_json):
    items = json.loads(root_json.read_text())
    schema = json.loads(_SCHEMA_PATH.read_text())
    parent = root_json.parent
    for an_item in items:
        name = an_item["name"].replace(" ", "-").lower()
        directory = parent / name
        if not directory.exists():
            continue
        for child in directory.glob("*.json"):
            print("Checking", child)
            try:
                _validate_json_file(child, schema)
            except InvalidFileError as exc:
                yield child, exc
