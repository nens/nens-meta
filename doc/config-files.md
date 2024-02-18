# The various config files


## Customisation and prevention of customisation

Nens-meta tries to be only as invasive as necessary and to get out of your way where possible. The config files have two basic customisation tweaks.

- If the literal text `NENS_META_LEAVE_ALONE`, in all caps, is found anywhere in a file, it is left alone. A similarly-named file with a `.suggestion` extension is written instead.

- Most files have an `### Extra lines below are preserved ###` line at the end. All content below it is preserved, ideal for custom content. `nens.toml` and `pyproject.toml` are excluded, they don't need it.


## `.nens.toml`



## `.editorconfig`

The generated setup in `.editorconfig` automatically strips extra spaces at the end of lines and adds an enter at the end of the file. Indentation with spaces in most spaces. Suggested max line lengths for python&co, unlimited line lengths for markdown.

Nothing earth-shaking, just some basic sanity for all the files. See https://editorconfig.org/ .

Many editors [have build-in support](https://editorconfig.org/#pre-installed), for some you need a plugin, [like for vscode](https://marketplace.visualstudio.com/items?itemName=EditorConfig.EditorConfig).

## `.gitignore`

## `pyproject.toml`

Pytest is installed via the "test extra dependencies" in [pyproject.toml](config-files.md#pyprojecttoml), so something like:

    [project.optional-dependencies]
    test = [
        "pytest",
        "pytest-mock",
    ]

## `tox.ini`

## `.pre-commit-config.yaml`

## `.github/dependabot.yml`

## `.github/workflows/meta_workflow.yml`

## `requirementx.txt`
