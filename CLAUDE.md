# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Status

This is an early-stage Python project. The only file currently present is `main.py` (empty). No build system, dependency manager, or test framework has been configured yet.

## Getting Started

Before writing code, establish a project foundation:

- Use `pyproject.toml` (with `uv` or `poetry`) or `requirements.txt` for dependency management
- Use `pytest` for testing
- Use `ruff` for linting and formatting

Typical commands once configured:

```bash
python main.py          # run the app
pytest                  # run all tests
pytest tests/test_x.py::test_name  # run a single test
ruff check .            # lint
ruff format .           # format
```
