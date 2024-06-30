import unittest
import json
import tempfile
from pathlib import Path
from hamcrest import assert_that, empty, has_length, instance_of, contains_exactly, has_item, anything
from surface_saver.validator import validate_all_json_files, InvalidFileError

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

        results = list(validate_all_json_files(root_json))
        assert_that(results, empty())

    def test_invalid_json_syntax(self):
        root_json = self.root_dir / "root.json"
        root_json.write_text(json.dumps([{"name": "Box One"}]))

        box_one = self.root_dir / "box-one"
        box_one.mkdir()
        invalid_file = box_one / "invalid.json"
        invalid_file.write_text("{invalid json")

        results = list(validate_all_json_files(root_json))
        assert_that(results, has_length(1))
        assert_that(results[0], has_item(invalid_file))
        assert_that(results[0], has_item(instance_of(InvalidFileError)))

    def test_missing_required_field(self):
        root_json = self.root_dir / "root.json"
        root_json.write_text(json.dumps([{"name": "Box One"}]))

        box_one = self.root_dir / "box-one"
        box_one.mkdir()
        missing_field_file = box_one / "missing_description.json"
        missing_field_file.write_text(json.dumps([
            {
                "name": "Item 1",
                "categories": ["Category A"]
            }
        ]))

        results = list(validate_all_json_files(root_json))
        assert_that(results, has_length(1))
        assert_that(results[0], has_item(missing_field_file))
        assert_that(results[0], has_item(instance_of(InvalidFileError)))

    def test_invalid_field_type(self):
        root_json = self.root_dir / "root.json"
        root_json.write_text(json.dumps([{"name": "Box One"}]))

        box_one = self.root_dir / "box-one"
        box_one.mkdir()
        invalid_type_file = box_one / "invalid_type.json"
        invalid_type_file.write_text(json.dumps([
            {
                "name": "Item 1",
                "categories": "Not an array",
                "description": "Description 1"
            }
        ]))

        results = list(validate_all_json_files(root_json))
        assert_that(results, has_length(1))
        assert_that(results[0], has_item(invalid_type_file))
        assert_that(results[0], has_item(instance_of(InvalidFileError)))

    def test_nonexistent_directory(self):
        root_json = self.root_dir / "root.json"
        root_json.write_text(json.dumps([{"name": "Nonexistent Box"}]))

        results = list(validate_all_json_files(root_json))
        assert_that(results, empty())

    def test_empty_directory(self):
        root_json = self.root_dir / "root.json"
        root_json.write_text(json.dumps([{"name": "Empty Box"}]))

        empty_box = self.root_dir / "empty-box"
        empty_box.mkdir()

        results = list(validate_all_json_files(root_json))
        assert_that(results, empty())

    def test_multiple_invalid_files(self):
        root_json = self.root_dir / "root.json"
        root_json.write_text(json.dumps([{"name": "Box One"}, {"name": "Box Two"}]))

        box_one = self.root_dir / "box-one"
        box_one.mkdir()
        invalid_file1 = box_one / "invalid1.json"
        invalid_file1.write_text("{invalid json")

        box_two = self.root_dir / "box-two"
        box_two.mkdir()
        invalid_file2 = box_two / "invalid2.json"
        invalid_file2.write_text(json.dumps([{"name": "Item 1"}]))  # Missing required 'description'

        results = sorted(validate_all_json_files(root_json))
        assert_that(results, has_length(2))
        assert_that(results[0], has_item(invalid_file1))
        assert_that(results[1], has_item(invalid_file2))
