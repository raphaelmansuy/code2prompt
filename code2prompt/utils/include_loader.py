import os
from jinja2 import BaseLoader, TemplateNotFound
import threading

class CircularIncludeError(Exception):
    pass

class IncludeLoader(BaseLoader):
    def __init__(self, path, encoding='utf-8'):
        self.path = path
        self.encoding = encoding
        self.include_stack = threading.local()

    def get_source(self, environment, template):
        path = os.path.join(self.path, template)
        if not os.path.exists(path):
            raise TemplateNotFound(template)
        
        if not hasattr(self.include_stack, 'stack'):
            self.include_stack.stack = []
        
        if path in self.include_stack.stack:
            raise CircularIncludeError(f"Circular include detected: {' -> '.join(self.include_stack.stack)} -> {path}")
        
        self.include_stack.stack.append(path)
        
        try:
            with open(path, 'r', encoding=self.encoding) as f:
                source = f.read()
        finally:
            self.include_stack.stack.pop()
        
        return source, path, lambda: True

    def list_templates(self):
        return []