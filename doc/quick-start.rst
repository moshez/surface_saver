Quickstart Guide
================

Surface Saver is a tool designed to help organize and validate your storage system.

Installation
------------

To install Surface Saver, use pip:

.. code-block:: bash

    pip install surface-saver

Basic Usage
-----------

Surface Saver provides a command-line interface for validating your JSON files. Here's how to use it:

1. Prepare your root JSON file (e.g., ``boxes.json``) in the following format:

   .. code-block:: json

       [
           {"name": "Box One"},
           {"name": "Box Two"}
       ]

2. Organize your JSON files in directories named after each box (with spaces replaced by hyphens and lowercased).

3. Run the validation command:

   .. code-block:: bash

       python -m surface_saver validate path/to/boxes.json

   This command will check all JSON files in the directories specified by ``boxes.json``.
   The directories are assumed to be relative to the ``boxes.json`` file.

Command-line Interface
----------------------

The ``validate`` command has the following syntax:

.. code-block:: none

    python -m surface_saver validate [-h] json_file

Arguments:
    json_file
        Path to the root JSON file that defines your box structure.

Options:
    -h, --help
        Show the help message and exit.

Output
------

If any files are invalid, the output will include one line per invalid file with an explanation. 
Each line will contain the file path and the specific problem encountered.

Example output for invalid files:

.. code-block:: none

    Error in file /path/to/box-one/item1.json: 'description' is a required property
    Error in file /path/to/box-two/item2.json: Invalid JSON syntax

For more detailed information on using Surface Saver, please refer to the full documentation.