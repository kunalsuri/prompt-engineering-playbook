# Python Development Standards

**Target Version: Python 3.12+**

## 1. Code Style & Quality

- **Strictly follow PEP 8**.
- **Type Hints**: Mandatory for all function parameters and return values. Use modern syntax (`list[str]`, `str | int`, `TypeAlias`).
- **Docstrings**: Use Google style for all functions/classes. Include `Args`, `Returns`, `Raises`, and examples for complex functions.
- **Formatting**: Use `ruff format` standards (a `black`-compatible formatter with built-in import sorting).
- **Strings**: Use f-strings exclusively.
- **Paths**: Use `pathlib.Path`, never string manipulation for paths.
- **Data Structures**: Prefer `dataclasses` over dictionaries for structured data.

## 2. Error Handling & Logging

- **Exceptions**: Use custom exception hierarchies. Never use bare `except:`.
- **Logging**: Use the `logging` module. Never use `print()` for production output.
- **Validation**: Validate inputs early (fail-fast principle).

## 3. Testing

- **Framework**: Use `pytest`.
- **Structure**: Use `conftest.py` for fixtures.
- **Mocking**: Use `unittest.mock` or `pytest-mock`.
- **Coverage**: Aim for high test coverage.

## 4. Project Standards

- **Config**: Use environment variables (`python-dotenv`, `pydantic-settings`). No hardcoded secrets.
- **Dependencies**: Manage via `pyproject.toml` or pinned `requirements.txt`.
- **Modern Idioms**: Use context managers (`with`), `enumerate`, `zip`, structural pattern matching, and the walrus operator (`:=`) where it improves readability.

## 5. Anti-Patterns to Avoid

- Mutable default arguments (e.g., `def func(x=[])`).
- String concatenation in loops (use `.join()`).
- Global variables.
- Bare `except:` clauses.

## 6. Enforcement

We use automated tooling to enforce these standards:

- **`ruff`**: Linting, import sorting, code formatting, and code quality
- **`mypy`**: Static type checking
- **`pytest`**: Testing

Configure these tools via `pyproject.toml` in your target project. Optionally, use a `.pre-commit-config.yaml` to run checks automatically on commit.
