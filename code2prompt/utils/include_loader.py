import os
from typing import List, Tuple, Callable
from jinja2 import BaseLoader, TemplateNotFound
import threading
from contextlib import contextmanager
import jinja2  # Import jinja2 to resolve the undefined name error


class CircularIncludeError(Exception):
    """Exception raised when a circular include is detected in templates."""

    pass


class IncludeLoader(BaseLoader):
    """
    A custom Jinja2 loader that supports file inclusion with circular dependency detection.

    This loader keeps track of the include stack for each thread to prevent circular includes.
    It raises a CircularIncludeError if a circular include is detected.

    Attributes:
        path (str): The base path for template files.
        encoding (str): The encoding to use when reading template files.
        include_stack (threading.local): Thread-local storage for the include stack.
    """

    def __init__(self, path: str, encoding: str = "utf-8"):
        """
        Initialize the IncludeLoader.

        Args:
            path (str): The base path for template files.
            encoding (str, optional): The encoding to use when reading template files. Defaults to 'utf-8'.
        """
        self.path: str = path
        self.encoding: str = encoding
        self.include_stack: threading.local = threading.local()

    @contextmanager
    def _include_stack_context(self, path):
        if not hasattr(self.include_stack, "stack"):
            self.include_stack.stack = set()
        if path in self.include_stack.stack:
            raise CircularIncludeError(f"Circular include detected: {path}")
        self.include_stack.stack.add(path)
        try:
            yield
        finally:
            self.include_stack.stack.remove(path)

    def get_source(
        self, environment: "jinja2.Environment", template: str
    ) -> Tuple[str, str, Callable[[], bool]]:
        path: str = os.path.join(self.path, template)
        if not os.path.exists(path):
            raise TemplateNotFound(f"{template} (searched in {self.path})")

        with self._include_stack_context(path):
            try:
                with open(path, "r", encoding=self.encoding) as f:
                    source: str = f.read()
            except IOError as e:
                raise TemplateNotFound(
                    template, message=f"Error reading template file: {e}"
                ) from e

        return source, path, lambda: True

    def list_templates(self) -> List[str]:
        """
        List all available templates.

        This method is not implemented for this loader and always returns an empty list.

        Returns:
            List[str]: An empty list.
        """
        return []
