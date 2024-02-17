# The tools being used

Note: only `tox` needs to be installed globally, the rest of the tools are included in the virtualenv or they are provided through calls to tox.

## Tox (for every project)

Tox is originally a test runner, but it is often used to run (and install) all sorts of project-related tools. The main advantage: it is an automation tool that runs on both linux, mac and windows. Just `pip install tox` and everything else is handled.

[The `tox.ini`](config-files.md#toxini) defines what can be run. "What can be run" is called an "environment", so the `-e` in calls like `tox -e coverage` means "select the coverage environment and run it".

Anyway, just calling `tox` will normally run the basic actions that github also runs in its checks. So of tox runs OK, github mostly won't complain.

**TODO**: add tox to the `requirements.txt` and just run it inside the virtualenv? Then no extra install is needed. The requirements.txt should be pretty small anyway as most of the dependencies ought to be in `pyproject.toml`. Perhaps attract a bit of attention to `tox -e dependencies`?


## Ruff (for python projects)

[Ruff](https://docs.astral.sh/ruff/) is black+flake8+isort+pyupgrade all in one. `ruff format` is mostly "black" and `ruff check` is all the rest. It only needs a bit of config in [pyproject.toml](config-files.md#pyprojecttoml).

You *can* run it on the commandline if you have it installed and you *can* install the ruff plugin for vscode that automatically formats your code when you save it.

On the commandline:

    $ ruff format
    $ ruff check --fix

It is also integrated into tox:

    $ tox -e lint
    $ tox -e format

What ruff actually does depends a lot on the configuration  [in pyproject.toml](config-files.md#pyprojecttoml). Especially the configured checks.


(pytest)=
## Pytest (for python projects)

[Pytest](https://docs.pytest.org) should installed via the "test extra dependencies" in [pyproject.toml](config-files.md#pyprojecttoml), so something like:

    [project.optional-dependencies]
    test = [
        "pytest",
        "pytest-mock",
    ]

Pytest is configured in that same `pyproject.toml`. It is basically the python test runner that everyone uses. Tests are discovered automatically when they're called `test_*.py` and they work with simple `assert` statements. Just look at [the test of nens-meta itself](https://github.com/nens/nens-meta/tree/main/nens_meta/tests).

Ask a programmer about a quick demo or read the [Pytest documentation](https://docs.pytest.org).

If the virtualenv is activated, pytest should just run as:

    $ pytest

Simple as that. Everything (like vscode) that recognises a virtualenv should be able to run pytest out of the box. There are a couple of handy tricks with pytest:

    $ pytest -l  # If a test fails, show the locally known variables.
    # pytest -x  # Stop immediately upon the first error: handy if you have many

Tox (without any options) also runs the tests that pytest runs, only with less verbosity and for (optionally) multiple python versions. The tests are the same, though.


## Coverage (for python projects)

Configured in `pyproject.toml`, run via `tox -e coverage`. Shows the coverage as a textual summary and generates `htmlcov/index.html` for a nice visual representation.

*If* configured to do so, coverage will warn you if the coverage is lower than the configured minimum level. In [.nens.toml](config-files.md#nenstoml), the `minimum_coverage` setting in `[tox]` can be set for this.


## Pre-commit

[Pre-commit](https://pre-commit.com/) (installed through tox) is a tool to run all sorts of checks and formatters on your code. The big advantage is that pre-commit itself handles the **installation** of the checkers and formatters so that you don't have to. Everything is done for you.

Even pre-commit doesn't need installing as "tox" does it for you.

**Optionally** you can insert it into your git workflow with `pre-commit install`, then pre-commit will run and will check your files before adding them to a commit. That's something for the serious programmers, probably, as when there's an error, getting past it might be a tad tricky.

Run it with:

    $ tox -e lint

This runs everything from ruff to spaces-at-the-end-of-lines checkers to yaml/toml syntax checkers.

TODO: ansible detection + pre-commit setup.


## Dependabot

Dependabot is a service build into github. [It does a lot of things](https://docs.github.com/en/code-security/dependabot/working-with-dependabot). nens-meta currently only uses it to update the versions of actions used in the github action workflow steps.

In the future, proper python/javascript dependency checking could be added. Though you can always enable it yourself if you want, of course.
