import logging
import colorlog

def setup_logger(level="INFO"):
    """Set up the logger with the specified logging level."""
    logger = colorlog.getLogger()
    logger.setLevel(level)

    # Create console handler
    ch = colorlog.StreamHandler()
    ch.setLevel(level)

    # Create formatter with a more structured format
    formatter = colorlog.ColoredFormatter(
        '%(log_color)s[%(asctime)s] %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    ch.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(ch)

    return logger

def log_error(message):
    """Log an error message."""
    logger = logging.getLogger()
    logger.error(message)

def log_output_created(output_path):
    """Log a message indicating that an output file has been created."""
    logger = logging.getLogger()
    logger.info(f"Output file created: {output_path}")

def log_clipboard_copy(success):
    """Log a message indicating whether copying to clipboard was successful."""
    logger = logging.getLogger()
    if success:
        logger.info("Content copied to clipboard successfully.")
    else:
        logger.error("Failed to copy content to clipboard.")

def log_token_count(token_count):
    """Log the token count."""
    logger = logging.getLogger()
    logger.info(f"Token count: {token_count}")
