# Changelog of nens-meta


## 0.1 (2024-02-18)

- Initial project structure created with cookiecutter and [cookiecutter-python-template](https://github.com/nens/cookiecutter-python-template).
- Generating an `.editorconfig` file in the target project.
- Started using a `.nens.toml` file for configuring our behaviour.
- Generating `.gitignore`.
- Generating `.pre-commit-config.yaml`.
- Generating `pyproject.toml`. Settings for ruff, zest.releaser, pytest, coverage and vscode.
- Renaming files that aren't needed anymore, such as `setup.py` :-)
- Generating basic `tox.ini`, mostly for python projects atm.
- Changed suggested virtualenv dir from `venv/` to `.venv/`.
- Using a single github workflow file.
- Minimum python version can now be configured.
- Most generated files have an "extra lines marker": lines after it are preserved when re-generating the content.
- If a file has `NENS_META_LEAVE_ALONE` somewhere in its context, it is left alone by the file generation mechanism.
- Added readthedocs configuration.
