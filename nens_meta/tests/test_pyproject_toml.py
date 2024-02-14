from pathlib import Path

import pytest

from nens_meta import pyproject_toml


@pytest.fixture
def empty_python_config(tmp_path: Path) -> pyproject_toml.PyprojectToml:
    pyproject_toml.create_if_missing(tmp_path)
    return pyproject_toml.PyprojectToml(tmp_path, {})


def test_pyproject_toml_file(tmp_path: Path):
    assert pyproject_toml.pyproject_toml_file(tmp_path).name == "pyproject.toml"


def test_create_if_missing(tmp_path: Path):
    pyproject_toml.create_if_missing(tmp_path)
    assert (tmp_path / "pyproject.toml").exists()


def test_read(empty_python_config: pyproject_toml.PyprojectToml):
    assert empty_python_config._contents == {}


def test_get_or_create_section(empty_python_config: pyproject_toml.PyprojectToml):
    empty_python_config.get_or_create_section("reinout")
    empty_python_config.write()
    assert "[reinout]" in empty_python_config._config_file.read_text()


def test_write_leave_alone(empty_python_config: pyproject_toml.PyprojectToml):
    # The test above already tested write, we test the leave alone setting
    empty_python_config.get_or_create_section("reinout")
    empty_python_config._options["leave_alone"] = True  # A bit hacky.
    empty_python_config.write()
    assert "[reinout]" not in empty_python_config._config_file.read_text()
    assert (
        "[reinout]"
        in (empty_python_config._project / "pyproject.toml.suggestion").read_text()
    )


def test_ensure_build_system(empty_python_config: pyproject_toml.PyprojectToml):
    empty_python_config.ensure_build_system()
    empty_python_config.write()
    assert "setuptools>=" in empty_python_config._config_file.read_text()


def test_adjust_project(empty_python_config: pyproject_toml.PyprojectToml):
    empty_python_config._options = {
        "project_name": "pietje",
    }
    empty_python_config.adjust_project()
    empty_python_config.write()
    assert "pietje" in empty_python_config._config_file.read_text()
    assert "dependencies" in empty_python_config._config_file.read_text()
