import logging
import re
from pathlib import Path

logger = logging.getLogger(__name__)

EXTRA_LINES_MARKER = "### Extra lines below are preserved ###\n"
EXTRA_LINES_MARKER_MARKDOWN = "<-- Extra lines below are preserved -->"


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


def handle_extra_lines(victim: Path, content: str) -> str:
    """Return content including extra lines marker and possible extra lines from target"""
    if victim.suffix == ".md":
        extra_lines_marker = EXTRA_LINES_MARKER_MARKDOWN
    else:
        extra_lines_marker = EXTRA_LINES_MARKER
    if extra_lines_marker not in content:
        content += extra_lines_marker
    original_content = victim.read_text()
    parts = original_content.split(extra_lines_marker)
    if len(parts) > 1:
        content += parts[1]
    return content


def write_if_changed(victim: Path, content: str):
    """Write content to file if different, not if it is the same

    And create the file if it doesn't exist.

    And... look for an end-of-generated-file marker and preserve the contents after it.

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
