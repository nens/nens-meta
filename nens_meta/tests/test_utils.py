from pathlib import Path

from pytest_mock.plugin import MockerFixture

from nens_meta import utils


def test_write_if_changed1(tmp_path: Path):
    # Just write something to a new file.
    f = tmp_path / "sample.txt"
    utils.write_if_changed(f, "test")
    assert f.exists()
    assert f.read_text() == "test"


def test_write_if_changed2(tmp_path: Path):
    # Write something new to an existing file.
    f = tmp_path / "sample.txt"
    f.write_text("bla bla")
    utils.write_if_changed(f, "test")
    assert f.read_text() == "test"


def test_write_if_changed3(tmp_path: Path, mocker: MockerFixture):
    # Don't change an existing file if it is not needed.
    f = tmp_path / "sample.txt"
    f.write_text("test")
    writer = mocker.spy(Path, "write_text")
    utils.write_if_changed(f, "test")
    writer.assert_not_called()


def test_is_python_project1():
    # We ourselves are a python project.
    ourselves = Path(__file__).parent.parent.parent
    assert utils.is_python_project(ourselves)


def test_is_python_project2(tmp_path: Path):
    # An empty dir is not a python project
    assert not utils.is_python_project(tmp_path)
