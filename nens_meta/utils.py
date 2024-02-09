import logging
from pathlib import Path

logger = logging.getLogger(__name__)


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
