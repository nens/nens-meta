"""Purpose: read and manage the pyproject.toml config file
"""
import logging
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

import tomlkit
from tomlkit.items import Table
from tomlkit.toml_document import TOMLDocument

from nens_meta import utils

FILENAME = "pyproject.toml"

logger = logging.getLogger(__name__)


def pyproject_toml_file(project: Path) -> Path:
    return project / FILENAME


def create_if_missing(project: Path):
    if not pyproject_toml_file(project).exists():
        pyproject_toml_file(project).write_text("# Initially generated by nens-meta\n")
        logger.info("Created empty pyproject.toml")


def write_documentation():
    options = {"project_name": "example-project", "package_name": "example_project"}
    target = Path(__file__).parent.parent / "doc" / "pyproject_toml_example.toml"
    with TemporaryDirectory() as project_dir:
        project_dir = Path(project_dir)
        package_dir = project_dir / "example_project"
        package_dir.mkdir()
        create_if_missing(project_dir)
        project_config = PyprojectToml(project_dir, options)
        project_config.update()
        project_config.write()
        project_config._config_file.replace(target)


class PyprojectToml:
    """Wrapper around a project's pyproject.toml"""

    _project: Path
    _config_file: Path
    _contents: tomlkit.TOMLDocument
    _options: dict

    def __init__(self, project: Path, options: dict):
        self._project = project
        self._config_file = pyproject_toml_file(project)
        self._options = options
        self._contents = self.read()

    def read(self) -> tomlkit.TOMLDocument:
        return tomlkit.parse(self._config_file.read_text())

    def write(self):
        target = self._project / FILENAME
        utils.write_if_changed(
            target, tomlkit.dumps(self._contents), handle_extra_lines=False
        )

    def get_or_create_section(self, name: str) -> Table:
        *super_tables, section_name = name.split(".")
        current_container: TOMLDocument | Table = self._contents
        for super_table in super_tables:
            if super_table not in current_container:  # type: ignore
                current_container.append(
                    super_table, tomlkit.table(is_super_table=True)
                )  # type: ignore
                logger.debug(f"Created section parent {super_table} for {name}")
            current_container = current_container[super_table]  # type: ignore

        if section_name not in current_container:
            current_container.append(section_name, tomlkit.table())
            logger.debug(f"Created section {name}")
        section: Table = current_container[section_name]  # type: ignore
        return section

    def update(self):  # pragma: no cover
        """Update the pyproject.toml file

        `options` is the combined contents of the [meta] and [pyprojecttoml] config
        sections.
        """

        self.adjust_build_system()
        self.adjust_project()
        self.adjust_setuptools()
        self.adjust_pytest()
        self.adjust_coverage()
        self.adjust_ruff()
        self.adjust_zestreleaser()
        self.adjust_pyright()
        self.remove_old_sections()

    def _suggest(self, section_name: str, key: str, value: Any, strongly=False):
        section = self.get_or_create_section(section_name)
        if key not in section:
            section[key] = value
            logger.info(f"pyproject.toml: suggesting [{section_name}]->{key}")
        if strongly:
            if section[key] != value:
                logger.info(
                    f"    Note: our suggested pyproject.toml value for [{section_name}]->{key}: {value}"
                )

    def _force(self, section_name: str, key: str, value: Any):
        section = self.get_or_create_section(section_name)
        if section.get(key) != value:
            section[key] = value
            logger.info(f"pyproject.toml: setting [{section_name}]->{key}")

    def adjust_build_system(self):
        section_name = "build-system"
        self._suggest(section_name, "requires", ["setuptools>=69"])

    def adjust_project(self):
        section_name = "project"
        self._force(section_name, "name", self._options["project_name"])

        self._suggest(section_name, "requires-python", ">=3.11")
        self._suggest(section_name, "dependencies", [])
        self._suggest(section_name, "description", "I really need to set this")
        self._suggest(section_name, "authors", [])
        self._suggest(section_name, "readme", "README.md")

        section = self.get_or_create_section("project.optional-dependencies")
        if "test" not in section:
            section["test"] = []
        test_dependencies: list = section["test"]  # type ignore
        if "pytest" not in test_dependencies:
            test_dependencies.append("pytest")
            section["test"].comment("pytest added by nens-meta")

    @property
    def package_name(self) -> str:
        name = self._options.get("package_name")
        if not name:
            logger.error("package_name not set in `.nens.toml` [meta]")
            name = "not_set"
        if not (self._project / name).exists():
            logger.error(f"Python package {name} doesn't exist in the current project")
        return name

    def adjust_setuptools(self):
        section_name = "tool.setuptools"
        # TODO: optional extra packages
        self._suggest(section_name, "packages", [self.package_name], strongly=True)

    def adjust_pytest(self):
        section_name = "tool.pytest.ini_options"
        self._force(
            section_name, "testpaths", [self.package_name]
        )  # TODO: optional extra packages
        self._suggest(section_name, "log_level", "DEBUG")

    def adjust_coverage(self):
        section_name = "tool.coverage.run"
        self._force(
            section_name, "source", [self.package_name]
        )  # TODO: optional extra packages

        section_name = "tool.coverage.report"
        self._force(section_name, "show_missing", True)
        self._force(section_name, "skip_empty", True)

    def adjust_ruff(self):
        section_name = "tool.ruff"
        self._suggest(section_name, "target-version", "py38")

        section_name = "tool.ruff.lint"
        self._suggest(section_name, "select", ["E4", "E7", "E9", "F", "I", "UP"])

    def adjust_pyright(self):
        section_name = "tool.pyright"
        self._force(
            section_name, "include", [self.package_name]
        )  # TODO: optional extra packages
        self._suggest(section_name, "venvPath", ".", strongly=True)
        self._suggest(section_name, "venv", ".venv", strongly=True)

    def adjust_zestreleaser(self):
        section_name = "tool.zest-releaser"
        self._suggest(section_name, "release", False)

    def move_outdated_files(self):
        """There are various old config files that have to be taken care off

        They shouldn't exist anymore as they can disturb our pyproject.toml
        configuration. But sometimes you need to copy over data (like from the
        setup.py), so they're best moved aside with a postfix.
        """
        for source_name in [".flake8", "setup.py", "setup.cfg", ".coveragerc"]:
            target_name = source_name + ".outdated"
            source = self._project / source_name
            if not source.exists():
                continue
            target = self._project / target_name
            if target.exists():
                target.unlink()
                logger.debug(f"Removed existing {target}")
            source.rename(target)
            logger.info(f"{source} is no longer needed, moved it to {target}")

    def remove_old_sections(self):
        """Remove sections of old tools.

        For instance, isort had a `[tool.isort]` section. That's now obsoleted by ruff.
        """
        tool_super_section = self._contents.get("tool")
        if tool_super_section:
            if "isort" in tool_super_section:
                tool_super_section.remove("isort")
                logger.info("Removed [tool.isort] section")


if __name__ == "__main__":
    # Only called to write the documentation file.
    write_documentation()
