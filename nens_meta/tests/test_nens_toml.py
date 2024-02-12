"""Tests for update_project.py"""
from pathlib import Path

import pytest

from nens_meta import nens_toml


def test_nens_toml_file(tmp_path: Path):
    assert nens_toml.nens_toml_file(tmp_path).name == ".nens.toml"


def test_create_if_missing(tmp_path: Path):
    nens_toml.create_if_missing(tmp_path)
    assert (tmp_path / ".nens.toml").exists()


def test_init(tmp_path: Path):
    nens_toml.nens_toml_file(tmp_path).write_text("year = 1972")
    config = nens_toml.OurConfig(tmp_path)
    assert config._contents["year"] == 1972


def test_write(tmp_path: Path):
    nens_toml.nens_toml_file(tmp_path).write_text("year = 1972")
    config = nens_toml.OurConfig(tmp_path)
    config._contents["month"] = 12
    config.write()
    assert "month = 12" in nens_toml.nens_toml_file(tmp_path).read_text()


def test_section_options1(tmp_path: Path):
    # Properly read a known variable in a known section.
    nens_toml.nens_toml_file(tmp_path).write_text(
        """
    [meta]
    version = "1972"
    """
    )
    config = nens_toml.OurConfig(tmp_path)
    assert config.section_options("meta")["version"] == "1972"


def test_section_options2(tmp_path: Path):
    # Barf upon an unknown/undocumented section.
    nens_toml.nens_toml_file(tmp_path).write_text(
        """
    [reinout]
    year = 1972
    """
    )
    config = nens_toml.OurConfig(tmp_path)
    with pytest.raises(nens_toml.MissingDocumentationError):
        config.section_options("reinout")


def test_section_options3(tmp_path: Path):
    # Don't return values that are unknown.
    nens_toml.nens_toml_file(tmp_path).write_text(
        """
    [meta]
    # Comment
    year = 1972
    """
    )
    config = nens_toml.OurConfig(tmp_path)
    assert "year" not in config.section_options("meta").keys()
