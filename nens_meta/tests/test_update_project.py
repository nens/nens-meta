"""Tests for update_project.py"""
from pathlib import Path

import pytest

from nens_meta import nens_toml, update_project


def test_check_prerequisites1(tmp_path: Path):
    with pytest.raises(SystemExit):
        # Missing .git/
        update_project.check_prerequisites(tmp_path)


def test_check_prerequisites2(tmp_path: Path):
    (tmp_path / ".git").mkdir()
    with pytest.raises(SystemExit):
        # Missing .nens.toml
        update_project.check_prerequisites(tmp_path)


# TemplatedFile is tested through EditorConfig, btw
def test_editor_config1(tmp_path: Path):
    # No config, check file contents.
    nens_toml.create_if_missing(tmp_path)
    our_config = nens_toml.OurConfig(tmp_path)
    editor_config = update_project.Editorconfig(tmp_path, our_config)
    assert "# Need extra lines?" in editor_config.content


def test_editor_config2(tmp_path: Path):
    # No config, check file contents of the written file
    nens_toml.create_if_missing(tmp_path)
    our_config = nens_toml.OurConfig(tmp_path)
    editor_config = update_project.Editorconfig(tmp_path, our_config)
    editor_config.write()
    assert "# Need extra lines?" in (tmp_path / ".editorconfig").read_text()


def test_editor_config3(tmp_path: Path):
    # We have extra_lines in the config, check file contents.
    (tmp_path / ".nens.toml").write_text(
        '''
    [editorconfig]
    extra_lines = """
    [*.reinout]
    max_line_length = 1972
    """
    '''
    )
    our_config = nens_toml.OurConfig(tmp_path)
    editor_config = update_project.Editorconfig(tmp_path, our_config)
    assert "# Need extra lines?" not in editor_config.content
    assert "max_line_length = 1972" in editor_config.content


def test_editor_config4(tmp_path: Path):
    # Don't change the file if told so.
    (tmp_path / ".nens.toml").write_text(
        """
    [editorconfig]
    leave_alone = true
    """
    )
    (tmp_path / ".editorconfig").write_text(
        """
    hurray, totally invalid line
    which would normally be overwritten
    """
    )
    our_config = nens_toml.OurConfig(tmp_path)
    editor_config = update_project.Editorconfig(tmp_path, our_config)
    editor_config.write()
    assert "hurray" in (tmp_path / ".editorconfig").read_text()


def test_tox_ini1(tmp_path: Path):
    # No config, check file contents.
    nens_toml.create_if_missing(tmp_path)
    our_config = nens_toml.OurConfig(tmp_path)
    tox_ini = update_project.ToxIni(tmp_path, our_config)
    assert "# Configure extra_lines" in tox_ini.content


def test_dependabot(tmp_path: Path):
    nens_toml.create_if_missing(tmp_path)
    our_config = nens_toml.OurConfig(tmp_path)
    dependabot_yml = update_project.DependabotYml(tmp_path, our_config)
    assert "extra_lines" in dependabot_yml.content
    dependabot_yml.write()


def test_metaworkflowyml(tmp_path: Path):
    nens_toml.create_if_missing(tmp_path)
    our_config = nens_toml.OurConfig(tmp_path)
    meta_workflow_yml = update_project.MetaWorkflowYml(tmp_path, our_config)
    assert "extra_lines" in meta_workflow_yml.content
    meta_workflow_yml.write()
