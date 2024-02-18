"""Purpose: read and manage the pyproject.toml config file
"""
import logging
from pathlib import Path
from tempfile import TemporaryDirectory

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

        # Naming convention: the "ensure_" methods mostly take complete ownership over a
        # section, the "adjust_" methods mostly leave everything intact and only changes
        # what's necessary.
        self.adjust_build_system()
        self.adjust_project()
        self.adjust_setuptools()
        self.ensure_pytest()
        self.ensure_coverage()
        self.adjust_ruff()
        self.adjust_zestreleaser()
        self.adjust_pyright()
        self.remove_old_sections()

    def adjust_build_system(self):
        section = self.get_or_create_section("build-system")
        section["requires"] = ["setuptools>=69"]
        section["requires"].comment("Suggested by nens-meta")

    def adjust_project(self):
        section = self.get_or_create_section("project")
        section["name"] = self._options["project_name"]
        section["name"].comment("Set by nens-meta")

        suggestions = {
            "requires-python": ">=3.11",
            "dependencies": [],
            "description": "I really need to set this",
            "authors": [],
            "readme": "README.md",
        }
        for suggestion in suggestions:
            if suggestion not in section:
                section[suggestion] = suggestions[suggestion]
                section[suggestion].comment("Suggested by nens-meta")

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
        section = self.get_or_create_section("tool.setuptools")
        # TODO: optional extra packages
        section["packages"] = [self.package_name]
        section["packages"].comment("Set by nens-meta")
        if "zip-safe" not in section:
            section["zip-safe"] = False

    def ensure_pytest(self):
        section = self.get_or_create_section("tool.pytest.ini_options")
        section["testpaths"] = [self.package_name]  # TODO: optional extra packages
        section["testpaths"].comment("Set by nens-meta")
        if "log_level" not in section:
            section["log_level"] = "DEBUG"
            section["log_level"].comment("Suggested by nens-meta")

    def ensure_coverage(self):
        section = self.get_or_create_section("tool.coverage.run")
        section["source"] = [self.package_name]  # TODO: optional extra packages
        section["source"].comment("Set by nens-meta")

        section = self.get_or_create_section("tool.coverage.report")
        section.comment("show_missing and skip_empty set by nens-meta")
        section["show_missing"] = True
        section["skip_empty"] = True

    def adjust_ruff(self):
        section = self.get_or_create_section("tool.ruff")
        if "target-version" not in section:
            section["target-version"] = "py38"
            section["target-version"].comment("Suggested by nens-meta")

        section = self.get_or_create_section("tool.ruff.lint")
        if "select" not in section:
            section["select"] = ["E4", "E7", "E9", "F", "I"]
            section["select"].comment(
                "Suggested by nens-meta, please add 'UP' and 'C901'"
            )

    def adjust_pyright(self):
        section = self.get_or_create_section("tool.pyright")
        section["include"] = [self.package_name]  # TODO: optional extra packages
        section["include"].comment("Set by nens-meta")
        section["venvPath"] = "."
        section["venvPath"].comment("Set by nens-meta")
        section["venv"] = ".venv"
        section["venv"].comment("Set by nens-meta")

    def adjust_zestreleaser(self):
        section = self.get_or_create_section("tool.zest-releaser")
        if "release" not in section:
            section["release"] = False
            section.comment("Suggested by nens-meta, adjust from setup.cfg if needed")

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
                logger.debug("Removed [tool.isort] section")


if __name__ == "__main__":
    # Only called to write the documentation file.
    write_documentation()
