import logging


def get_logger(name: str, log_level: int = logging.WARNING) -> logging.Logger:
    """
    Create and return a logger with a specific format: time | lvl | module | func | line.

    :param name: Name of the logger, typically the module name.
    :param log_level: Log level to set for the logger (default is logging.WARNING).
    :return: Configured logger object.
    """
    # Create a logger object
    logger = logging.getLogger(name)

    # Set the log level
    logger.setLevel(log_level)

    # Define the log format
    log_format = "%(asctime)s | %(levelname)s | %(module)s | %(funcName)s | %(lineno)d"

    # Create a formatter with the specified format
    formatter = logging.Formatter(log_format)

    # Create a console handler to output to stdout
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    # Add the handler to the logger
    if not logger.handlers:  # Avoid duplicate handlers
        logger.addHandler(handler)

    return logger


main_logger = get_logger(name='main', log_level=logging.WARNING)
