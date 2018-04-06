# Edge Development Tools

I used a bunch of scripts for maintaining my [Edge][edge] project. They are:

* `buildtest.py`: One-shot end-to-end test from generating a project to running tests
* `templatify.py`: Escape a normal HTML template for startproject templates
* `update-requirements.py`: Updates all requirements.txt files from Pipenv output

## Install

Make sure your local Edge project repository and this devtools repository directories are side-by-side i.e. they are inside the same parent directory.

For instance this directory structure is correct:

    └── my-edge
        ├── edge
        └── edge-devtools

Read Edge documentation to find out how to setup virtual environment for Edge. All scripts are assumed to be running inside the Edge virtual environment.

[edge]: https://github.com/arocks/edge
