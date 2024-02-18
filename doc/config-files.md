# The various config files


## Customisation and prevention of customisation

Nens-meta tries to be only as invasive as necessary and to get out of your way where possible. The config files have two basic customisation tweaks.

- If the literal text `NENS_META_LEAVE_ALONE`, in all caps, is found anywhere in a file, it is left alone. A similarly-named file with a `.suggestion` extension is written instead.

- Most files have an `### Extra lines below are preserved ###` line at the end. All content below it is preserved, ideal for custom content. `.nens.toml` and `pyproject.toml` are excluded, they don't need it.


## `.nens.toml`

The file for our own configuration. The defaults are below:

```{literalinclude} nens_toml_example.toml
```

## `.editorconfig`

The generated setup in `.editorconfig` automatically strips extra spaces at the end of lines and adds an enter at the end of the file. Indentation with spaces in most spaces. Suggested max line lengths for python&co, unlimited line lengths for markdown.

Nothing earth-shaking, just some basic sanity for all the files. See https://editorconfig.org/ .

Many editors [have build-in support](https://editorconfig.org/#pre-installed), for some you need a plugin, [like for vscode](https://marketplace.visualstudio.com/items?itemName=EditorConfig.EditorConfig).


## `.gitignore`

Just a basic set of ignores.


## `pyproject.toml`

The now-standard configuration file for python projects. Previously, most of the content would have been in `setup.py` and/or `setup.cfg`, but those aren't needed anymore.

There are many settings in this file, so nens-meta leaves it **mostly** alone so that you can have your own custom content in there. Many tools have their configuration in here:

- coverage
- pyright/pylance
- pytest
- ruff
- setuptools
- z3c.dependencychecker
- zest.releaser

In an empty project, nens-meta generates the following default settings:

```{literalinclude} pyproject_toml_example.toml
```


## `tox.ini`

## `.pre-commit-config.yaml`

## `.github/dependabot.yml`

## `.github/workflows/meta_workflow.yml`

## `requirementx.txt`
