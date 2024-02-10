# N&S "meta" repository

Modeled after https://github.com/plone/meta , it is a tool to keep lots of repositories up to date regarding minutia such as "editorconfig", "ruff", "pre-commit" and "github actions". Stuff that's often generated once with a cookiecutter and never afterwards modified, even though there's much goodness to be found in new settings.

The settings and config files go hand in hand with some recommended local settings in your development environment, like recommended vscode extensions.

The basic idea is **make it easy to write clean and neat and correct code without making the process irritating**. Installing vscode's "editorconfig" plugin once is hardly a chore. If a project's editorconfig file then prevents you from ever having to worry about lineendings, trailing spaces, indentation and other non-content-related stuff... that's a win.

Note that [our cookiecutter template](https://github.com/nens/cookiecutter-python-template) normally should have been the basis from which you started your project. But it might have been created by hand. Or it might have been a long time ago. "Meta" tries to fix up your project a bit.


## Editconfig

Install vscode's editorconfig plugin. Lots of other editors have build-in support or have their own plugin.

The generated setup in `.editorconfig` automatically strips extra spaces at the end of lines and adds an enter at the end of the file. Indentation with spaces in most spaces. Suggested max line lengths for python&co, unlimited line lengths for markdown.


## Installing the project

The regular:

    $ python3 -m venv venv
    $ . venv/bin/activate
    $ pip install -r requirements.txt

This gives you:

    $ update-project YOUR_PROJECT_DIR

At the moment, run the tests like this (after activating the virtualenv):

    $ pytest

And the isort/black/etc stuff that's in "ruff" now:

    $ pre-commit run --all

(You can also actually install the pre-commit to run it automatically, though that means you really have to behave yourself):

    $ pre-commit install


## TODO

- `DEVELOPING.md` with instructions?

- pre-commit: this needs "do I have python? do I have ansible?" detection. And a github update action. And a lint action. The ruff settings really need configuration, which means pyproject.toml support.

- tox.ini for python projects

- docker-compose
