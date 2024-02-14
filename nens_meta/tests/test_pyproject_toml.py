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


def test_get_or_create_section1(empty_python_config: pyproject_toml.PyprojectToml):
    empty_python_config.get_or_create_section("reinout")
    empty_python_config.write()
    assert "[reinout]" in empty_python_config._config_file.read_text()


def test_get_or_create_section(empty_python_config: pyproject_toml.PyprojectToml):
    empty_python_config.get_or_create_section("reinout.van")
    empty_python_config.write()
    assert "[reinout.van]" in empty_python_config._config_file.read_text()


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


def test_package_name1(empty_python_config: pyproject_toml.PyprojectToml):
    # Default case
    empty_python_config._options = {
        "package_name": "pietje_klaasje",
    }
    assert empty_python_config.package_name == "pietje_klaasje"


def test_package_name2(empty_python_config: pyproject_toml.PyprojectToml):
    # package_name not set, we get a default dummy one
    assert empty_python_config.package_name == "not_set"


def test_ensure_setuptools1(empty_python_config: pyproject_toml.PyprojectToml):
    empty_python_config._options = {
        "project_name": "pietje-klaasje",
        "package_name": "pietje_klaasje",
    }
    empty_python_config.ensure_setuptools()
    empty_python_config.write()
    assert "zip-safe" in empty_python_config._config_file.read_text()
    assert "pietje_klaasje.__version__" in empty_python_config._config_file.read_text()


def test_ensure_setuptools2(empty_python_config: pyproject_toml.PyprojectToml):
    # Corner case: init file without version.
    package_dir = empty_python_config._project / "pietje_klaasje"
    package_dir.mkdir()
    (package_dir / "__init__.py").write_text("# Empty")
    empty_python_config._options = {
        "project_name": "pietje-klaasje",
        "package_name": "pietje_klaasje",
    }
    empty_python_config.ensure_setuptools()
    # No assert needed.


def test_ensure_setuptools1pytest(empty_python_config: pyproject_toml.PyprojectToml):
    empty_python_config._options = {
        "package_name": "pietje_klaasje",
    }
    empty_python_config.ensure_pytest()
    empty_python_config.write()
    assert "log_level" in empty_python_config._config_file.read_text()
    assert '["pietje_klaasje"]' in empty_python_config._config_file.read_text()


def test_ensure_coverage(empty_python_config: pyproject_toml.PyprojectToml):
    empty_python_config._options = {
        "package_name": "pietje_klaasje",
    }
    empty_python_config.ensure_coverage()
    empty_python_config.write()
    assert "source" in empty_python_config._config_file.read_text()
    assert "pietje_klaasje" in empty_python_config._config_file.read_text()


def test_ensure_ruff(empty_python_config: pyproject_toml.PyprojectToml):
    empty_python_config._options = {
        "package_name": "pietje_klaasje",
    }
    empty_python_config.ensure_ruff()
    empty_python_config.write()
    assert "[tool.ruff.lint]" in empty_python_config._config_file.read_text()
    assert "target-version" in empty_python_config._config_file.read_text()


def test_ensure_pyright(empty_python_config: pyproject_toml.PyprojectToml):
    empty_python_config._options = {
        "package_name": "pietje_klaasje",
    }
    empty_python_config.adjust_pyright()
    empty_python_config.write()
    assert "[tool.pyright]" in empty_python_config._config_file.read_text()
    assert "pietje_klaasje" in empty_python_config._config_file.read_text()
