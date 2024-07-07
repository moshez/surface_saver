Surface Saver
=============

Surface Saver is a tool designed to help organize and validate your storage system. It provides a simple way to keep track of items in various storage boxes and ensures that your inventory data is correctly formatted.

Installation
------------

Surface Saver is available on PyPI. You can install it using pip:

.. code-block:: bash

    pip install surface_saver

Quick Start
-----------

1. Create a root JSON file (e.g., ``boxes.json``) listing your storage boxes:

   .. code-block:: json

       [
           {"name": "Box One"},
           {"name": "Box Two"}
       ]

2. For each box, create a directory (e.g., ``box-one``, ``box-two``) containing JSON files that describe the items in that box.

3. Validate your storage system:

   .. code-block:: bash

       python -m surface_saver validate path/to/boxes.json

   This command will check all JSON files in the directories specified by ``boxes.json`` and report any validation errors.

Features
--------

- Organize items into named boxes
- Validate JSON files against a predefined schema
- Command-line interface for easy validation

Documentation
-------------

For more detailed information and advanced usage, please refer to the full documentation in the ``docs`` directory.

Contributing
------------

Contributions are welcome! Please feel free to submit a Pull Request.

License
-------

This project is licensed under the MIT License. See the LICENSE file for details.