# NenS-meta: basic project configuration and automation

**Core idea**: update N&S projects so that the basics are up to date.

- `pyproject.toml` and `uv` for better installs (`requirements.txt` was often out of date or incomplete, `uv` makes good update behaviour way easier).
- Pre-commit for syntax checks and a bit of automatic cleanup without much hassle.
- Simple github action with basic checks.
- Explanation/documentation of the various files.
- Hints for vscode.

You should have installed `uv` by now (see [our documentation](tools.md#uv)). You can update a project by running:

```console
$ uvx nens-meta
```

**Second idea**, but not implemented yet: some administration. There's a `.nens.toml` file and I intend to put an optional project number in there. Then we can start to correlate some of our 500 github projects with projects that aren't active anymore, for instance. And we can start grouping github projects by type ("dashboard", "prefect", etc).

:::{note}
NenS-meta is mostly intended for use within https://www.nelen-schuurmans.nl, so the defaults are those that are handy for *our* projects.
:::

## Documentation contents

```{toctree}
self
background.md
tools.md
config-files.md
```
