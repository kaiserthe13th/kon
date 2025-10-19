# Running tests for this project

This project uses `uv` for managing a project-local virtual environment. The tests live in the `tests/` directory and use `pytest`.

```console
$ uv sync
...
$ uv tool run pytest
================ test session starts ================
...
================ AB passed in C.DEs =================
```
