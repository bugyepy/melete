# AI Contributor Guidelines

These instructions apply to the entire repository.

## Coding Style
- Follow PEP 8 conventions.
- Limit lines to 79 characters.
- Provide docstrings for all public functions and classes in English.

## Commit Guidelines
- Keep commits focused on a single change or feature.
- Update `README.md` when adding new user-facing features or commands.

## Programmatic Checks
- Before committing, run the following command to ensure all Python files
  compile:
  ```bash
  python -m py_compile $(git ls-files '*.py')
  ```

