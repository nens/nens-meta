"""Tests for update_project.py"""
from pathlib import Path

from nens_meta import nens_toml


def test_nens_toml_file(tmp_path: Path):
    assert nens_toml.nens_toml_file(tmp_path).name == ".nens.toml"


def test_create_if_missing(tmp_path: Path):
    nens_toml.create_if_missing(tmp_path)
    assert (tmp_path / ".nens.toml").exists()


def test_init(tmp_path: Path):
    nens_toml.nens_toml_file(tmp_path).write_text("year = 1972")
    config = nens_toml.Config(tmp_path)
    assert config._contents["year"] == 1972


def test_write(tmp_path: Path):
    nens_toml.nens_toml_file(tmp_path).write_text("year = 1972")
    config = nens_toml.Config(tmp_path)
    config._contents["month"] = 12
    config.write()
    assert "month = 12" in nens_toml.nens_toml_file(tmp_path).read_text()
