import logging
import sys

# Verbosity level constants
VERBOSITY_INFO = 1
VERBOSITY_DEBUG = 2


def setup_logging(verbose_count: int) -> None:
    """Set up logging based on verbosity level."""
    if verbose_count == 0:
        level = logging.WARNING
    elif verbose_count == VERBOSITY_INFO:
        level = logging.INFO
    elif verbose_count == VERBOSITY_DEBUG:
        level = logging.DEBUG
    else:
        level = logging.DEBUG

    logging.basicConfig(
        level=level, format="%(levelname)s: %(message)s", stream=sys.stderr
    )


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance."""
    return logging.getLogger(name)
