import unittest
import json
import tempfile
from pathlib import Path
from hamcrest import assert_that, raises, calling, has_properties, contains_string
from surface_saver import validate_all_json_files, InvalidFileError, _SCHEMA_PATH

class TestSurfaceSaverValidator(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root_dir = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_valid_files(self):
        root_json = self.root_dir / "root.json"
        root_json.write_text(json.dumps([
            {"name": "Box One"},
            {"name": "Box Two"}
        ]))

        box_one = self.root_dir / "box-one"
        box_one.mkdir()
        (box_one / "2023-06-30.json").write_text(json.dumps([
            {
                "name": "Item 1",
                "categories": ["Category A"],
                "description": "Description 1",
                "notes": "Note 1"
            }
        ]))

        box_two = self.root_dir / "box-two"
        box_two.mkdir()
        (box_two / "2023-07-01.json").write_text(json.dumps([
            {
                "name": "Item 2",
                "categories": ["Category B", "Category C"],
                "description": "Description 2"
            }
        ]))

        # This should not raise any exceptions
        validate_all_json_files(root_json)

    def test_invalid_json_syntax(self):
        root_json = self.root_dir / "root.json"
        root_json.write_text(json.dumps([{"name": "Box One"}]))

        box_one = self.root_dir / "box-one"
        box_one.mkdir()
        (box_one / "invalid.json").write_text("{invalid json")

        assert_that(
            calling(validate_all_json_files).with_args(root_json),
            raises(InvalidFileError)
        )

    def test_missing_required_field(self):
        root_json = self.root_dir / "root.json"
        root_json.write_text(json.dumps([{"name": "Box One"}]))

        box_one = self.root_dir / "box-one"
        box_one.mkdir()
        (box_one / "missing_description.json").write_text(json.dumps([
            {
                "name": "Item 1",
                "categories": ["Category A"]
            }
        ]))

        assert_that(
            calling(validate_all_json_files).with_args(root_json),
            raises(InvalidFileError)
        )

    def test_invalid_field_type(self):
        root_json = self.root_dir / "root.json"
        root_json.write_text(json.dumps([{"name": "Box One"}]))

        box_one = self.root_dir / "box-one"
        box_one.mkdir()
        (box_one / "invalid_type.json").write_text(json.dumps([
            {
                "name": "Item 1",
                "categories": "Not an array",
                "description": "Description 1"
            }
        ]))

        assert_that(
            calling(validate_all_json_files).with_args(root_json),
            raises(InvalidFileError)
        )

    def test_nonexistent_directory(self):
        root_json = self.root_dir / "root.json"
        root_json.write_text(json.dumps([{"name": "Nonexistent Box"}]))

        # This should not raise any exceptions
        validate_all_json_files(root_json)

    def test_empty_directory(self):
        root_json = self.root_dir / "root.json"
        root_json.write_text(json.dumps([{"name": "Empty Box"}]))

        empty_box = self.root_dir / "empty-box"
        empty_box.mkdir()

        # This should not raise any exceptions
        validate_all_json_files(root_json)

    def test_schema_exists(self):
        assert_that(_SCHEMA_PATH.exists(), "Schema file does not exist")

    def test_schema_is_valid_json(self):
        try:
            schema = json.loads(_SCHEMA_PATH.read_text())
        except json.JSONDecodeError:
            self.fail("Schema is not valid JSON")
