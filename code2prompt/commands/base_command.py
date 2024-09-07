# code2prompt/commands/base_command.py

from abc import ABC, abstractmethod
import logging
from code2prompt.config import Configuration

class BaseCommand(ABC):
    """
    Abstract base class for all commands in the code2prompt tool.

    This class defines the basic structure and common functionality
    for all command classes. It ensures that each command has access
    to the configuration and a logger, and defines an abstract execute
    method that must be implemented by all subclasses.

    Attributes:
        config (Configuration): The configuration object for the command.
        logger (logging.Logger): The logger instance for the command.
    """

    def __init__(self, config: Configuration, logger: logging.Logger):
        """
        Initialize the BaseCommand with configuration and logger.

        Args:
            config (Configuration): The configuration object for the command.
            logger (logging.Logger): The logger instance for the command.
        """
        self.config = config
        self.logger = logger

    @abstractmethod
    def execute(self) -> None:
        """
        Execute the command.

        This method must be implemented by all subclasses to define
        the specific behavior of each command.

        Raises:
            NotImplementedError: If the subclass does not implement this method.
        """
        raise NotImplementedError("Subclasses must implement execute method")

    def log_start(self) -> None:
        """
        Log the start of the command execution.
        """
        self.logger.info(f"Starting execution of {self.__class__.__name__}")

    def log_end(self) -> None:
        """
        Log the end of the command execution.
        """
        self.logger.info(f"Finished execution of {self.__class__.__name__}")

    def handle_error(self, error: Exception) -> None:
        """
        Handle and log any errors that occur during command execution.

        Args:
            error (Exception): The exception that was raised.
        """
        self.logger.error(f"Error in {self.__class__.__name__}: {str(error)}", exc_info=True)

    def validate_config(self) -> bool:
        """
        Validate the configuration for the command.

        This method should be overridden by subclasses to perform
        command-specific configuration validation.

        Returns:
            bool: True if the configuration is valid, False otherwise.
        """
        return True