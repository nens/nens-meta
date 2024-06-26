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

See https://packaging.python.org/en/latest/guides/writing-pyproject-toml/ for the syntax.

There are many settings in this file, so nens-meta leaves it **mostly** alone so that you can have your own custom content in there. Many tools have their configuration in here:

- coverage, see https://coverage.readthedocs.io/en/latest/config.html .
- pyright/pylance
- pytest, see https://docs.pytest.org/en/stable/reference/customize.html .
- ruff, see https://docs.astral.sh/ruff/configuration/ for defaults.
- setuptools, see https://setuptools.pypa.io/en/latest/userguide/pyproject_config.html .
- z3c.dependencychecker, see https://pypi.org/project/z3c.dependencychecker/#ignore-packages .
- zest.releaser, see https://zestreleaser.readthedocs.io/en/latest/options.html .

In an empty project, nens-meta generates the following default settings:

```{literalinclude} pyproject_toml_example.toml
```

There are three types of settings:

- The settings not mentioned here: nens-meta doesn't touch them, feel free to add and adjust them as needed.
- The `# Suggested by nens-meta` settings. They should be present and nens-meta suggests a default value, but you're free to change it.
- The `# Set by nens-meta` settings. They'll be overwritten when you let nens-meta update your project. So they're governed by [settings in `.nens.toml`](config-files.md#nenstoml).
  - `project_name`
  - `package_name` is used in several places where a list of the project's package dirs with the source code in it is needed.


## `.pre-commit-config.yaml`

By default, a few standard pre-commit checkers like `trailing-whitespace` and `check-yaml` are run. For python projects, [](tools.md#ruff) is added.


## `.github/dependabot.yml`

We want dependabot to keep our github actions up to date regarding the versions of the actions.


## `.github/workflows/meta_workflow.yml`

A basic workflow that runs pre-commit. If it is a python project, also pytest is run.

If you've set `[meta] > mimum_coverage` in [`.nens.toml`](config-files.md#nenstoml), the coverage is also generated and reported.


## `requirements.txt`

We really need a line like `-e .[test]` in there.


## `requirements.yml`

If you use ansible, you probably use modules like `community.general`. If [](tools.md#ansible-lint) starts complaining , add such modules to `requirements.yml. An example:

```yaml
# Extra ansible packages (used to get ansible-lint to find everything in
# github actions).
---
collections:
  - name: community.general
    version: ">=8.3.0"
  - name: ansible.posix
```
