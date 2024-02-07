import typer
from pathlib import Path
from typing_extensions import Annotated
import tomlkit
import logging


META_FILENAME = ".nens.toml"

logger = logging.getLogger(__name__)


class Pyprojecttoml:
    """Wrapper around a project's pyproject.toml"""

    meta_file: Path
    meta_config: tomlkit.TOMLDocument

    def __init__(self, project: Path) -> None:
        self.meta_file = project / META_FILENAME
        if not self.meta_file.exists():
            logger.warn(f"{self.meta_file} doesn't exist, we'll create it")
            self.meta_file.write_text("# Empty generated file\n")
        self.meta_config = self.read()
        print(self.meta_config)

    def read(self) -> tomlkit.TOMLDocument:
        return tomlkit.parse(self.meta_file.read_text())

    def write(self):
        self.meta_file.write_text(tomlkit.dumps(self.meta_config))


def update_project(
    project: Annotated[Path, typer.Argument(exists=True)],
):
    pyprojecttoml = Pyprojecttoml(project)


def main():
    typer.run(update_project)
