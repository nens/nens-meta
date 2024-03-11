# How to work on projects with this setup


## All projects: install pre-commit

For all the basic syntax checking and formatting:

```console
$ pip install pre-commit
$ pre-commit run --all
```


## Initial python virtualenv (for python projects)

Virtualenvs keep your global python installation nice and clean. They also help code completion.

- Create the virtualenv in the `.venv` dir. This is a convention that's also picked up by vscode.
- Activate it when working on the project.
- Install the requirements.

Here's how:

```console
$ python3 -m venv .venv
$ .venv/bin/activate         # <== On windows
$ source .venv/bin/activate  # <== On linux/mac
$ pip install -r requirements.txt
```

When you change requirements or dependencies in `pyproject.toml`, rerun the "pip install". Working on a project again after a time?: don't forget to activate again.


## VScode

- Install the [editorconf plugin](https://marketplace.visualstudio.com/items?itemName=EditorConfig.EditorConfig).
