import typer
from pathlib import Path
from typing_extensions import Annotated
import tomllib


META_FILENAME = ".nens.toml"


def update_project(
        project: Annotated[Path, typer.Argument(exists=True)],
):
    meta_file = project / META_FILENAME
    if not meta_file.exists():
        raise RuntimeError(f"{meta_file} doesn't exist")
    meta_config = tomllib.loads(meta_file.read_text())
    print(meta_config)


def main():
    typer.run(update_project)
