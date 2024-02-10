import logging
import sys
from functools import cached_property
from pathlib import Path
from typing import Annotated

import jinja2
import typer

from nens_meta import nens_toml, utils

TEMPLATES_BASEDIR = Path(__file__).parent / "templates"

logger = logging.getLogger(__name__)


class TemplatedFile:
    project_dir: Path
    our_config: nens_toml.OurConfig
    template_name: str
    target_name: str  # Note: can be "subdir/some-file.txt"
    section_name: str

    def __init__(self, project_dir: Path, our_config: nens_toml.OurConfig) -> None:
        self.project_dir = project_dir
        self.our_config = our_config

    @property
    def target(self) -> Path:
        return self.project_dir / self.target_name

    @property
    def environment(self) -> jinja2.Environment:
        return jinja2.Environment(
            loader=jinja2.FileSystemLoader(
                # pass one or more dirs! Handy for our purpose!
                [TEMPLATES_BASEDIR / "default"]
            ),
            keep_trailing_newline=True,
            trim_blocks=True,
            lstrip_blocks=True,
        )

    @property
    def template(self) -> jinja2.Template:
        return self.environment.get_template(self.template_name)

    @property
    def options(self) -> dict:
        return self.our_config.section_options(self.section_name)

    @cached_property
    def content(self) -> str:
        return self.template.render(**self.options)

    def write(self):
        """Copy the source template to the target, doing the jinja2 stuff"""
        utils.write_if_changed(self.target, self.content)


class Editorconfig(TemplatedFile):
    """Wrapper around a project's editorconfig"""

    template_name = "editorconfig.j2"
    target_name = ".editorconfig"
    section_name = "editorconfig"


def check_prerequisites(project_dir: Path):
    """Check prerequisites, exit if not met"""
    if not (project_dir / ".git").exists():
        logger.error("Project has no .git dir")
        sys.exit(1)
    if not nens_toml.nens_toml_file(project_dir).exists():
        nens_toml.create_if_missing(project_dir)
        logger.warning("No .nens.toml found, created one. Re-run after checking.")
        sys.exit(1)


def update_project(
    project_dir: Annotated[Path, typer.Argument(exists=True)],
    verbose: Annotated[bool, typer.Option(help="Verbose logging")] = False,
):
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=log_level)
    check_prerequisites(project_dir)
    our_config = nens_toml.OurConfig(project_dir)
    our_config.write()
    # ^^^ TODO: handle versions!
    # Grab editorconfig table and pass it along. Or rather the whole thing?
    editorconfig = Editorconfig(project_dir, our_config)
    editorconfig.write()


def main():
    typer.run(update_project)


# Option: typer.lauch("https://reinout/documentation")...
