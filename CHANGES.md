# Changelog of nens-meta


## 0.5 (unreleased)

- Simplified everything by removing tox for now.



## 0.4 (2024-02-20)


- Removed "tox -e format", we only use "tox -e lint" in practice.
- Detecting `ansible/` directory and adding ansible-lint to the pre-commit config if found.

## 0.3 (2024-02-20)

- In `tox.ini`, marking `sh` commands with a dash. This allows failure of those commands on windows. Later on a python wrapper can be written.
- Using github action's "matrix include" to explicitly set python/tox_env combinations. This results in a much shorter workflow file as all the tox setup steps are the same.
- Simplification: removed some advanced environments from `tox.ini` to keep the default generated file more clear.
- Simplification: removed header from most of the generated files. We don't need to be that "intrusive".
- Simplification: `.nens.toml` and `pyproject.toml` are handled in a much less invasive way. Removed most of the comments. Doing suggestions instead of changes. Etcetera.

## 0.2 (2024-02-19)


- The generated header doesn't include the version number anymore: that resulted in unnecessary changes.
- The generated header in config files now points at the config file documentation page at https://nens-meta.readthedocs.io/en/latest/config-files.html .
- Fixed `coverage --fail-under` behaviour if no percentage was specified.


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
