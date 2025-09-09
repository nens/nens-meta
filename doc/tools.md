# The tools being used


## uv

`uv` is a python virtualenv helper, tool installer, requirements tool and more. It really helps fix the mess with `python -m venv .`, outdated `requirements.txt`, globally installed tools/libraries, etc.

Documentation: https://docs.astral.sh/uv/

Installation instructions: https://docs.astral.sh/uv/getting-started/installation/

Every few months, an update is handy:

```console
$ uv self update
```

Some `uv` usage examples:

```console
$ uv sync            # Creates a virtualenv and installs the dependencies
$ uv run python      # Run python
$ uv run some/script.py
$ uv run manage.py migrate
$ uv add requests    # Add a requirement
$ uv run pytest
$ uv sync --upgrade  # Upgrade dependencies
```

`uv run` automatically updates your virtualenv when needed.

The virtualenv is stored in the `.venv/` directory, you can activate it if that fits your workflow.


## Pre-commit

[Pre-commit](https://pre-commit.com/) is *the* tool to run all sorts of checks and formatters on your code. The big advantage is that pre-commit itself handles the **installation** of the checkers and formatters so that you don't have to. Everything is done for you.

```console
$ uv tool install --upgrade pre-commit  # Global installation
$ pip install pre-commit                # *Old* installation method

$ pre-commit run --all                  # Just run this in every project
```

**Optionally** you can insert it into your git workflow with `pre-commit install`, then pre-commit will run and will check your files before adding them to a commit. That's something for the "hard-core" programmers, probably, as when there's an error, getting past it might be a tad tricky.

Pre-commit runs everything from ruff to spaces-at-the-end-of-lines checkers to yaml/toml syntax checkers. The configuration happens in [.pre-commit-config.yaml](./config-files.md#pre-commit-configyaml).


## Ruff

[Ruff](https://docs.astral.sh/ruff/) is black+flake8+isort+pyupgrade all in one. `ruff format` is mostly "black" and `ruff check` is all the rest. It only needs a bit of config in [pyproject.toml](config-files.md#pyprojecttoml). Normally, the only thing you need to run is this:

```console
$ pre-commit run --all  # Yes, this runs ruff, too
```

What ruff actually does depends a lot on the configuration  [in pyproject.toml](config-files.md#pyprojecttoml). Especially the configured checks. Do you want your python code upgraded to a newer syntax with f-strings (`UP`)? Automatic complexity checking (`C901`)?

You *can* run it on the commandline **if** you have it installed globally and you *can* install the ruff plugin for vscode that automatically formats your code when you save it.

```console
$ ruff format       # Just the "black" visual part
$ ruff check        # Syntax checks
$ ruff check --fix  # Safe fixes for syntax errors
```

## Pytest

[Pytest](https://docs.pytest.org) is the best test runner. Nicer to work with than python's standard `unittest` framework. Tests are discovered automatically when they're called `test_*.py` and they work with simple `assert` statements. Just look at [the test of nens-meta itself](https://github.com/nens/nens-meta/tree/main/src/nens_meta/tests). Ask a programmer about a quick demo or read the [Pytest documentation](https://docs.pytest.org).

```console
(.venv) $ pytest     # Note: activate the virtualenv!
(.venv) $ pytest -l  # Show local variables when there's an error
(.venv) $ pytest -x  # Stop immediately upon the first error
```

Everything (like vscode) that recognises a virtualenv should be able to run pytest out of the box.


## Coverage

TODO, resurrect "createcoverage" for this.

Configured in `pyproject.toml`, run via `tox -e coverage`. Shows the coverage as a textual summary and generates `htmlcov/index.html` for a nice visual representation.

*If* configured to do so, coverage will warn you if the coverage is lower than the configured minimum level. In [.nens.toml](config-files.md#nenstoml), the `minimum_coverage` setting in `[tox]` can be set for this.


## Ansible-lint

When an `ansible/` dir is found, [ansible-lint](https://ansible.readthedocs.io/projects/lint) is added to the pre-commit config.

See [](config-files.md#requirementsyml) for necessary configuration.


## Github actions

In the `main/master` branch and in pull requests, a `nens-meta` github action is automatically run. At least pre-commit. If you're a python project also pytest. If you've configured coverage, that too.

The way everything is set up hopefully makes working with this kind of checks easier and more comfortable.

If you need more: you can have nens-meta ignore the workflow file and customize it fully. And you can always add a second workflow file next to it.


## Dependabot

Dependabot is a service build into github. [It does a lot of things](https://docs.github.com/en/code-security/dependabot/working-with-dependabot). nens-meta currently only uses it to update the versions of actions used in the github action workflow steps.

In the future, proper python/javascript dependency checking could be added. Though you can always enable it yourself if you want, of course.


## VScode

Install the [editorconf plugin](https://marketplace.visualstudio.com/items?itemName=EditorConfig.EditorConfig). This helps automatically removing unnecessary empty lines at the end of files and spaces at the end of lines: stuff that Reinout or pre-commit will complain about. Just install the plugin and everything is handled for you.

If you use the default python plugin, add the following to your `pyproject.toml`, it helps vscode get the code completion and type hints right:

```toml
[tool.pyright]
# Pyright/pylance/vscode configuration.
include = ["src"]
venvPath = "."
venv = ".venv"
```
