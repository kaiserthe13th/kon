# Running tests for this project

This project uses `uv` for managing a project-local virtual environment. The tests live in the `tests/` directory and use `pytest`.

Quick local steps (PowerShell)

## Create a project venv using uv

uv venv

## Activate the venv (PowerShell)

.\.venv\Scripts\Activate.ps1

## Install test tooling into the venv

python -m pip install --upgrade pip pytest

## Run tests

pytest -q

Alternative (run without activating):

## Create venv

uv venv

## Run pytest through the venv python directly

.\.venv\Scripts\python -m pytest -q

Notes

- If you prefer the uv "tool" command for a global pytest installation you can use `uv tool install pytest` and then `uv tool run pytest`, but installing pytest into the project venv keeps test tooling local to the project.
- If your system Python differs from the project's required Python version, `uv venv` will create a `.venv` with a managed Python when available (see `uv` docs).
