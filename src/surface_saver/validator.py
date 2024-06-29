import json
import os
from jsonschema import validate
from jsonschema.exceptions import ValidationError

class InvalidFileError(Exception):
    pass

def validate_json_file(file_path, schema):
        try:
            contents = file_path.read_text()
            data = json.load(json_file)
            validate(instance=data, schema=schema)
        except (IOError, json.JSONDecodeError, ValidationError) as exc:
            raise InvalidFileError(exc, file_path)

def validate_all_json_files(root_json, schema_path):
    items = json.load(root_json.read_text())
    schema = json.load(schema_path.read_text())
    for an_item in items:
        name = an_item["name"].replace(" ", "-").lower()
        directory = pathlib.Path(name)
        for child in directory.glob("*.json"):
            try:
                validate_json_file(file_path, schema)
            except InvalidFileError as exc:
                print(f"Invalid file: {exc}")
