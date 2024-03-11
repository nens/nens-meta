import logging
import sys
from functools import cached_property
from pathlib import Path
from typing import Annotated

import jinja2
import typer

from nens_meta import nens_toml, pyproject_toml, utils

TEMPLATES_BASEDIR = Path(__file__).parent / "templates"

logger = logging.getLogger(__name__)


HEADER = """\
# Generated by nens-meta.
# See https://nens-meta.readthedocs.io/en/latest/config-files.html for info.
# If you want this file to be left alone, add "nens_meta_leave_alone" in
# all caps somewhere in this file in a comment.
#
"""


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

    def extra_options(self) -> dict:
        """Overwrite in subclasses to return some extra calculated options"""
        return {}

    @cached_property
    def our_options(self) -> dict:
        if not self.our_config.has_section_for(self.section_name):
            return {}
        return self.our_config.section_options(self.section_name)

    @cached_property
    def meta_options(self) -> dict:
        return self.our_config.section_options("meta")

    @cached_property
    def options(self) -> dict:
        result = {}
        result.update(self.meta_options)
        result.update(self.our_options)
        result.update(self.extra_options())
        return result

    @property
    def header(self) -> str:
        return HEADER.format(
            section_name=self.section_name, meta_version=self.options["meta_version"]
        )

    @cached_property
    def content(self) -> str:
        rendered = self.template.render(
            header=self.header,
            **self.options,
        )
        return utils.strip_whitespace(rendered)

    def create_dirs_if_needed(self):
        *directories, _ = self.target_name.split("/")
        if directories:
            target_dir = self.project_dir / "/".join(directories)
            if target_dir.exists():
                return
            target_dir.mkdir(parents=True)
            logger.info(f"Created directory {target_dir}")

    def write(self):
        """Copy the source template to the target, doing the jinja2 stuff"""
        self.create_dirs_if_needed()
        utils.write_if_changed(self.target, self.content)


class Editorconfig(TemplatedFile):
    """Wrapper around a project's editorconfig"""

    template_name = "editorconfig.j2"
    target_name = ".editorconfig"
    section_name = "editorconfig"


class Gitignore(TemplatedFile):
    """Wrapper around a project's gitignore"""

    template_name = "gitignore.j2"
    target_name = ".gitignore"
    section_name = "gitignore"


class Precommitconfig(TemplatedFile):
    """Wrapper around a project's .pre-commit-config.yaml"""

    template_name = "pre-commit-config.yaml.j2"
    target_name = ".pre-commit-config.yaml"
    section_name = "pre-commit-config"


class DependabotYml(TemplatedFile):
    """Wrapper around a dependabot.yml file"""

    template_name = "dependabot.yml.j2"
    target_name = ".github/dependabot.yml"
    section_name = "dependabot"


class MetaWorkflowYml(TemplatedFile):
    """Wrapper around a nens-meta.yml file"""

    template_name = "meta_workflow.yml.j2"
    target_name = ".github/workflows/nens-meta.yml"
    section_name = "meta_workflow"


def check_prerequisites(project_dir: Path):
    """Check prerequisites, exit if not met"""
    if not (project_dir / ".git").exists():
        logger.error("Project has no .git dir")
        sys.exit(1)
    if not nens_toml.nens_toml_file(project_dir).exists():
        nens_toml.create_if_missing(project_dir)
        logger.warning("No .nens.toml found, created one. Re-run after checking.")
        sys.exit(1)


def do_some_python_checks(project_dir: Path):
    """Run some checks to help identify issues and things you still need to do"""
    requirementstxt = project_dir / "requirements.txt"
    if not requirementstxt.exists():
        logger.warning(f"There is no {requirementstxt}")
    else:
        dev_indicator1 = "-e "
        dev_indicator2 = "[test]"
        if not (
            dev_indicator1 in requirementstxt.read_text()
            and dev_indicator2 in requirementstxt.read_text()
        ):
            logger.warning(
                f"The text '{dev_indicator1}' and '{dev_indicator2}' are "
                f"not both found in {requirementstxt}"
            )
        if "coverage" not in requirementstxt.read_text():
            logger.warning("You might want to add 'coverage' to requirements.txt")
    for file_to_check in project_dir.glob("*.outdated"):
        logger.warning(
            f"Check the old {file_to_check}: move settings to pyproject.toml, perhaps?"
        )
    website = "https://nens-meta.readthedocs.io"
    readme = Path("README.md")
    if readme.exists():
        if website not in readme.read_text():
            logger.warning(
                f"{website} is not mentioned in the readme as an instruction"
            )


def update_project(
    project_dir: Annotated[Path, typer.Argument(exists=True)],
    verbose: Annotated[bool, typer.Option(help="Verbose logging")] = False,
):  # pragma: no cover
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=log_level, format="%(levelname)-7s: %(message)s")
    check_prerequisites(project_dir)
    our_config = nens_toml.OurConfig(project_dir)
    our_config.write()

    if our_config.section_options("meta")["is_python_project"]:
        if not pyproject_toml.pyproject_toml_file(project_dir).exists():
            pyproject_toml.create_if_missing(project_dir)
        options_for_project_config = {}
        options_for_project_config.update(our_config.section_options("meta"))
        options_for_project_config.update(our_config.section_options("pyprojecttoml"))
        project_config = pyproject_toml.PyprojectToml(
            project_dir, options_for_project_config
        )
        project_config.update()
        project_config.write()
        project_config.move_outdated_files()

    # Grab editorconfig table and pass it along. Or rather the whole thing?
    editorconfig = Editorconfig(project_dir, our_config)
    editorconfig.write()
    gitignore = Gitignore(project_dir, our_config)
    gitignore.write()
    precommitconfig = Precommitconfig(project_dir, our_config)
    precommitconfig.write()
    dependabot_yml = DependabotYml(project_dir, our_config)
    dependabot_yml.write()
    meta_workflow_yml = MetaWorkflowYml(project_dir, our_config)
    meta_workflow_yml.write()

    if our_config.section_options("meta")["is_python_project"]:
        do_some_python_checks(project_dir)


def main():  # pragma: no cover
    typer.run(update_project)
