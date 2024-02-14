"""Purpose: read and manage the .nens.toml config file
"""
import logging
from pathlib import Path

import tomlkit
from tomlkit.items import Table

from nens_meta import __version__, utils

META_FILENAME = ".nens.toml"
LEAVE_ALONE = "leave_alone_FALSE"
LEAVE_ALONE_EXPLANATION = "Do not change the file, only put a *.suggestion next to it"
KNOWN_SECTIONS: dict[str, dict[str, str]] = {}
# First key is the section name, the second key/value pair is the variable name and the
# explanation. If the second key ends with "_TRUE"/"_FALSE", this is stripped and will
# be used to treat the value as a boolean with the indicated default.
KNOWN_SECTIONS["meta"] = {
    "meta_version": "Version used to generate the config",
    "project_name": "Project name (normally the name of the directory)",
    "is_python_project_FALSE": "Whether we are a python project",
}
KNOWN_SECTIONS["editorconfig"] = {
    "extra_lines": "Extra content at the end of `.editorconfig`",
    LEAVE_ALONE: LEAVE_ALONE_EXPLANATION,
}
KNOWN_SECTIONS["tox"] = {
    "minimum_coverage": "Minimum code coverage percentage",
    LEAVE_ALONE: LEAVE_ALONE_EXPLANATION,
}
KNOWN_SECTIONS["pre-commit-config"] = {
    "extra_lines": "Extra content at the end of the file (watch the indentation)",
    LEAVE_ALONE: LEAVE_ALONE_EXPLANATION,
}
KNOWN_SECTIONS["gitignore"] = {
    "extra_lines": "Extra content at the end of `.gitignore`",
    LEAVE_ALONE: LEAVE_ALONE_EXPLANATION,
}
KNOWN_SECTIONS["development-instructions"] = {
    "extra_lines": "Extra content at the end of `DEVELOPMENT.md`",
    LEAVE_ALONE: LEAVE_ALONE_EXPLANATION,
}
logger = logging.getLogger(__name__)


def nens_toml_file(project: Path) -> Path:
    return project / META_FILENAME


def create_if_missing(project: Path):
    assert not nens_toml_file(project).exists()
    nens_toml_file(project).write_text("# Initially generated by nens-meta\n")


def _key_name(key: str) -> str:
    """Return key, but handle the _TRUE/_FALSE postfix tricks"""
    for indicates_boolean in ["_TRUE", "_FALSE"]:
        if indicates_boolean in key:
            return key.replace(indicates_boolean, "")
    return key


def _default_for_key(key: str) -> str | bool:
    """Return default (''), but handle the _TRUE/_FALSE postfix tricks"""
    if "_TRUE" in key:
        return True
    if "_FALSE" in key:
        return False
    return ""


def _expected_type(key: str) -> type:
    """Return expected type of the key"""
    for indicates_boolean in ["_TRUE", "_FALSE"]:
        if indicates_boolean in key:
            return bool
    return str


def detected_meta_values(project: Path) -> dict[str, str | bool]:
    """Return values we can detect about the project, normally set in [meta]"""
    detected: dict[str, str | bool] = {}
    detected["is_python_project"] = utils.is_python_project(project)
    detected["meta_version"] = __version__
    detected["project_name"] = project.resolve().name
    return detected


class MissingDocumentationError(Exception):
    pass


class OurConfig:
    """Wrapper around a project's .nens.toml

    See https://tomlkit.readthedocs.io/en/latest/quickstart/
    """

    _config_file: Path
    _contents: tomlkit.TOMLDocument
    _project: Path

    def __init__(self, project: Path):
        self._project = project
        self._config_file = nens_toml_file(project)
        self._contents = self.read()
        self.update_meta_options()

    def read(self) -> tomlkit.TOMLDocument:
        return tomlkit.parse(self._config_file.read_text())

    def write(self):
        utils.write_if_changed(self._config_file, tomlkit.dumps(self._contents))

    def update_meta_options(self):
        """Detect meta options"""
        if "meta" not in self._contents:
            self._contents.append("meta", tomlkit.table())
        current: Table = self._contents["meta"]  # type: ignore
        detected = detected_meta_values(self._project)
        for key, value in detected.items():
            if key not in current:
                current[key] = value
        # Make sure our version is correctly recorded
        current["meta_version"] = detected["meta_version"]

    def section_options(self, section_name: str) -> dict:
        """Return all options configured in a given section

        Later on: perhaps do some filtering on known ones? And add defaults for missing
        ones?

        """
        if section_name not in KNOWN_SECTIONS:
            # Force ourselves to document our stuff!
            raise MissingDocumentationError(
                f"Section {section_name} not documented in nens-meta"
            )
        section = self._contents.get(section_name)
        options: dict[str, str | bool] = {}
        if section:
            for key in KNOWN_SECTIONS[section_name]:
                actual_key_name = _key_name(key)
                value = section.get(actual_key_name, _default_for_key(key))
                if not isinstance(value, _expected_type(key)):
                    raise ValueError(
                        f"{actual_key_name} should be of type {_expected_type(key)}, not {type(value)}"
                    )
                options[actual_key_name] = value

        else:
            logger.debug(
                f"Extra configuration for [{section_name}] not found in .nens.toml"
            )
        logger.debug(f"Contents of section {section_name}: {options}")
        return options
