"""Tests for update_project.py"""
from nens_meta import update_project


def test_nens_toml_init_creates_file(tmp_path):
    update_project.NensToml(tmp_path)
    assert (tmp_path / ".nens.toml").exists()
