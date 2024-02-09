"""Tests for update_project.py"""
from pathlib import Path

import pytest

from nens_meta import update_project


def test_check_prerequisites1(tmp_path: Path):
    with pytest.raises(SystemExit):
        # Missing .git/
        update_project.check_prerequisites(tmp_path)


def test_check_prerequisites2(tmp_path: Path):
    (tmp_path / ".git").mkdir()
    with pytest.raises(SystemExit):
        # Missing .nens.toml
        update_project.check_prerequisites(tmp_path)
        # ... which should be created for us now.
        assert (tmp_path / ".nens.tomll").exists()
