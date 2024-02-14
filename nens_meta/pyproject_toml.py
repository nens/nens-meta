"""Purpose: read and manage the pyproject.toml config file
"""
import logging
from pathlib import Path

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
        target_name = FILENAME
        if self._options.get("leave_alone"):
            logger.warning(f"Leaving {target_name} alone")
            target_name += ".suggestion"
        target = self._project / target_name
        utils.write_if_changed(target, tomlkit.dumps(self._contents))

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

    def update(self):
        """Update the pyproject.toml file

        `options` is the combined contents of the [meta] and [pyprojecttoml] config
        sections.
        """

        self.ensure_build_system()
        self.adjust_project()
        self.ensure_setuptools()

    def ensure_build_system(self):
        section = self.get_or_create_section("build-system")
        section.clear()
        section.comment("Whole section managed by nens-meta")
        section["requires"] = ["setuptools>=69"]

    def adjust_project(self):
        section = self.get_or_create_section("project")
        section["name"] = self._options["project_name"]
        section["name"].comment("Set by nens-meta")
        section["dynamic"] = ["version"]
        section["dynamic"].comment("Set by nens-meta")

        suggestions = {
            "requires-python": ">=3.11",
            "dependencies": [],
        }
        for suggestion in suggestions:
            if suggestion not in section:
                section[suggestion] = suggestions[suggestion]
                section[suggestion].comment("Suggested by nens-meta")

        section = self.get_or_create_section("project.optional-dependencies")
        if "test" not in section:
            section["test"] = []
        if "pytest" not in section["test"]:
            section["test"].append("pytest")
        section["test"].comment("pytest added by nens-meta")

        section = self.get_or_create_section("project.optional-dependencies")
        if "test" not in section:
            section["test"] = []
        if "pytest" not in section["test"]:
            section["test"].append("pytest")
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

    def ensure_setuptools(self):
        section = self.get_or_create_section("tool.setuptools")
        section.clear()
        section.comment("Whole section managed by nens-meta")
        # TODO: optional extra packages
        section["packages"] = [self.package_name]
        section["zip-safe"] = False

        section = self.get_or_create_section("tool.setuptools.dynamic")
        section.clear()
        section.comment("Whole section managed by nens-meta")
        version_data = tomlkit.inline_table()
        version_data.update({"attr": f"{self.package_name}.__version__"})
        section["version"] = version_data
        init_file = self._project / self.package_name / "__init__.py"
        if init_file.exists():
            if "__version__" not in init_file.read_text():
                logger.error(f"__version__ not set in {init_file}, add it there")
        else:
            logger.error(f"{init_file} doesn't exist, add __version__ in there")
