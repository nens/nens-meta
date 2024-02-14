import logging
import re
from pathlib import Path

logger = logging.getLogger(__name__)


def strip_whitespace(content: str) -> str:
    """Return content stripped of EOL whitespace and extra EOF linefeeds

    Generating files using jinja2 template tags sometimes result in such unneeded
    whitespace. Stripping it off afterwards is easier than trying to get it right with
    jinja2.
    """
    # Get rid of spaces at the end of lines.
    content = re.sub(r"\ +\n", r"\n", content)
    # Get rid of empty lines at the end.
    content = content.strip() + "\n"
    return content


def write_if_changed(victim: Path, content: str):
    """Write content to file if different, not if it is the same

    And create the file if it doesn't exist.
    """
    if victim.exists():
        action = "Updated"
        existing_content = victim.read_text()
        if content == existing_content:
            logger.debug(f"{victim} remained the same")
            return
    else:
        action = "Created"

    victim.write_text(content)
    logger.info(f"{action} {victim}")


def is_python_project(project: Path) -> bool:
    """Return whether we detect a python project"""
    for indicator in ["setup.py", "pyproject.toml", "setup.cfg"]:
        if (project / indicator).exists():
            logger.debug(f"{indicator} found, assuming it is a python project")
            return True
    return False
