import logging
from pathlib import Path
from typing import Annotated

import jinja2
import tomlkit
import typer

from nens_meta import utils

META_FILENAME = ".nens.toml"
CONFIG_BASEDIR = Path(__file__).parent / "config"

logger = logging.getLogger(__name__)


class NensToml:
    """Wrapper around a project's .nens.toml

    See https://tomlkit.readthedocs.io/en/latest/quickstart/
    """

    meta_file: Path
    meta_config: tomlkit.TOMLDocument

    def __init__(self, project: Path) -> None:
        self.meta_file = project / META_FILENAME
        if not self.meta_file.exists():
            logger.warning(f"{self.meta_file} doesn't exist, we'll create it")
            self.meta_file.write_text("# Empty generated file\n")
        self.meta_config = self.read()

    def read(self) -> tomlkit.TOMLDocument:
        return tomlkit.parse(self.meta_file.read_text())

    def write(self):
        utils.write_if_changed(self.meta_file, tomlkit.dumps(self.meta_config))


class Editorconfig:
    """Wrapper around a project's editorconfig"""

    target: Path
    template_name: str = "editorconfig.j2"

    def __init__(self, project: Path) -> None:
        self.target = project / ".editorconfig"

    def write(self):
        """Copy the source template to the target, doing the jinja2 stuff"""
        environment = jinja2.Environment(
            loader=jinja2.FileSystemLoader(
                # pass one or more dirs! Handy for our purpose!
                [CONFIG_BASEDIR / "default"]
            ),
            variable_start_string="%(",
            variable_end_string=")s",
            keep_trailing_newline=True,
            trim_blocks=True,
            lstrip_blocks=True,
        )
        template = environment.get_template(self.template_name)
        content = template.render()
        utils.write_if_changed(self.target, content)

    # try:
    #     options = get_properties(filename)
    # except EditorConfigError:
    #     print "Error occurred while getting EditorConfig properties"


def update_project(
    project: Annotated[Path, typer.Argument(exists=True)],
):
    nenstoml = NensToml(project)
    nenstoml.write()
    # ^^^ TODO: handle versions!
    # Grab editorconfig table and pass it along. Or rather the whole thing?
    editorconfig = Editorconfig(project)
    editorconfig.write()


def main():
    logging.basicConfig(level=logging.DEBUG)
    typer.run(update_project)
