# How to use it

Most of the projects will be python projects, so follow the virtualenv instructions further below.

As the root automation tool, we use `tox`, so to start with do a global install with pip/pipx/whatever:

    $ pip install tox


## Basic usage

In the end, just running [tox](tools.md#tox) is enough:

    $ tox

This runs the syntax checkers, the tests and whatever is most needed. In [.nens.toml](config-files.md#nenstoml), the `default_environments` setting in `[tox]` defines what is most necessary.

There are some commands/environments that are standard that you can run separately:

    $ tox -e format  # just formatting of your code
    $ tox -e lint    # linting, more serious checks

Anyway, just run "tox" unless it is especially handy to select an individual environment. Or if it is handy to run `pytest -x` or `ruff check` or so.


## Initial python virtualenv (for python projects)

Virtualenvs keep your global python installation nice and clean. They also help code completion.

- Create the virtualenv in the `.venv` dir. This is a convention that's also picked up by vscode.
- Activate it when working on the project.
- Install the requirements

Here's how:

    $ python3 -m venv .venv
    $ .venv/bin/activate         # <== On windows
    $ source .venv/bin/activate  # <== On linux/mac
    $ pip install -r requirements.txt

When you change requirements or dependencies in `pyproject.toml`, rerun the "pip install". Working on a project again after a time?: don't forget to activate again.


## Python testing: pytest

Just run:

    $ pytest

That'll discover your `test_*.py` or `*_test.py` files inside `nens_meta`.

VScode's big "run the tests" button should also automatically run it.

See [the tools documentation](tools.md#pytest) for more pytest tips.


## VScode

- Install the [editorconf plugin](https://marketplace.visualstudio.com/items?itemName=EditorConfig.EditorConfig).


## Emacs and other editors

Yes, Reinout uses [emacs](https://www.gnu.org/software/emacs/), an editor older than himself. Literally. Emacs has the company beaten by at least two decades. But the basic ideas apply to all other editors.
