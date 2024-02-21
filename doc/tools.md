# The tools being used

Note: only `tox` needs to be installed globally, the rest of the tools are included in the virtualenv or they are provided through calls to tox.

## Tox

Tox is originally a test runner, but it is often used to run (and install) all sorts of project-related tools. The main advantage: it is an automation tool that runs on both linux, mac and windows. Just `pip install tox` and everything else is handled.

:::{important}
Tox is the only program **you really need to install by hand** globally. So don't forget the `pip install tox`. All the rest is handled and installed by tox.
:::


[The `tox.ini`](config-files.md#toxini) defines what can be run. "What can be run" is called an "environment", so the `-e` in calls like `tox -e coverage` means "select the coverage environment and run it". Anyway, just calling `tox` will normally run the basic actions that github also runs in its checks. So of tox runs OK, github mostly won't complain.

```console
$ tox           # Run all the important bits.
$ tox -e lint   # Run a specific 'environment'
$ tox -qe lint  # -q quiets down the tox output a bit
$ tox list      # List all available 'environments'
$ tox -r        # Rebuild whatever tox cached: cleanup
```


## Ruff

[Ruff](https://docs.astral.sh/ruff/) is black+flake8+isort+pyupgrade all in one. `ruff format` is mostly "black" and `ruff check` is all the rest. It only needs a bit of config in [pyproject.toml](config-files.md#pyprojecttoml).

```console
$ tox               # Tox by default also runs ruff
$ tox -e lint       # Lint runs both ruff format and check
```

What ruff actually does depends a lot on the configuration  [in pyproject.toml](config-files.md#pyprojecttoml). Especially the configured checks. Do you want your python code upgraded to a newer syntax with f-strings? Automatic complexity checking?

You *can* run it on the commandline **if** you have it installed globally and you *can* install the ruff plugin for vscode that automatically formats your code when you save it.

```console
$ ruff format       # Just the "black" visual part
$ ruff check        # Syntax checks
$ ruff check --fix  # Safe fixes for syntax errors
```


## Pytest

[Pytest](https://docs.pytest.org) is the best test runner. Nicer to work with than python's standard `unittest` framework. Tests are discovered automatically when they're called `test_*.py` and they work with simple `assert` statements. Just look at [the test of nens-meta itself](https://github.com/nens/nens-meta/tree/main/nens_meta/tests). Ask a programmer about a quick demo or read the [Pytest documentation](https://docs.pytest.org).

```console
$ tox                # Runs tests for all configured python versions
$ tox -e py310       # Run the tests only with python 3.10
(.venv) $ pytest     # Note: activate the virtualenv!
(.venv) $ pytest -l  # Show local variables when there's an error
(.venv) $ pytest -x  # Stop immediately upon the first error
```

Everything (like vscode) that recognises a virtualenv should be able to run pytest out of the box. Note: for readability's sake, tox's pytest output is a bit shorter than when you run pytest directly.

## Coverage

Configured in `pyproject.toml`, run via `tox -e coverage`. Shows the coverage as a textual summary and generates `htmlcov/index.html` for a nice visual representation.

*If* configured to do so, coverage will warn you if the coverage is lower than the configured minimum level. In [.nens.toml](config-files.md#nenstoml), the `minimum_coverage` setting in `[tox]` can be set for this.


## Pre-commit

[Pre-commit](https://pre-commit.com/) (installed through tox) is a tool to run all sorts of checks and formatters on your code. The big advantage is that pre-commit itself handles the **installation** of the checkers and formatters so that you don't have to. Everything is done for you.

Even pre-commit doesn't need installing as "tox" does it for you.

**Optionally** you can insert it into your git workflow with `pre-commit install`, then pre-commit will run and will check your files before adding them to a commit. That's something for the "hard-core" programmers, probably, as when there's an error, getting past it might be a tad tricky.

```console
$ tox          # Tox by itself also runs 'lint'
$ tox -e lint  # "Lint" calls pre-commit
```

Pre-commit runs everything from ruff to spaces-at-the-end-of-lines checkers to yaml/toml syntax checkers. The configuration happens in [.pre-commit-config.yaml](./config-files.md#pre-commit-configyaml).


## Ansible-lint

When an `ansible/` dir is found, [ansible-lint](https://ansible.readthedocs.io/projects/lint) is added to the pre-commit config.

See [](config-files.md#requirementsyml) for necessary configuration.


## Github actions

In the `main/master` branch and in pull requests, a `nens-meta` github action is automatically run. What gets tested/checked there is is the same as what should be done if you just run `tox` locally.

The way everything is set up hopefully makes working with this kind of checks easier and more comfortable.


## Dependabot

Dependabot is a service build into github. [It does a lot of things](https://docs.github.com/en/code-security/dependabot/working-with-dependabot). nens-meta currently only uses it to update the versions of actions used in the github action workflow steps.

In the future, proper python/javascript dependency checking could be added. Though you can always enable it yourself if you want, of course.
