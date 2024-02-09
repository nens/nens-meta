import logging
import sys
from pathlib import Path
from typing import Annotated

import jinja2
import typer

from nens_meta import nens_toml, utils

TEMPLATES_BASEDIR = Path(__file__).parent / "templates"

logger = logging.getLogger(__name__)


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
                [TEMPLATES_BASEDIR / "default"]
            ),
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


def check_prerequisites(project: Path):
    """Check prerequisites, exit if not met"""
    if not (project / ".git").exists():
        logger.error("Project has no .git dir")
        sys.exit(1)
    if not nens_toml.nens_toml_file(project).exists():
        nens_toml.create_if_missing(project)
        logger.warning("No .nens.toml found, created one. Re-run after checking.")
        sys.exit(1)


def update_project(
    project: Annotated[Path, typer.Argument(exists=True)],
):
    check_prerequisites(project)
    config = nens_toml.Config(project)
    config.write()
    # ^^^ TODO: handle versions!
    # Grab editorconfig table and pass it along. Or rather the whole thing?
    editorconfig = Editorconfig(project)
    editorconfig.write()


def main():
    logging.basicConfig(level=logging.DEBUG)
    typer.run(update_project)
