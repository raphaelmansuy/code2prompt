from typing import OrderedDict
from jinja2 import Template, Environment, FileSystemLoader
from prompt_toolkit import prompt
import re

def load_template(template_path):
    """
    Load a Jinja2 template from a file.

    Args:
        template_path (str): Path to the template file.

    Returns:
        str: The contents of the template file.
    """
    try:
        with open(template_path, 'r') as file:
            return file.read()
    except IOError as e:
        raise IOError(f"Error loading template file: {e}")


def get_user_inputs(template_content):
    """
    Extract user-defined variables from the template and prompt for input.
    Args:
        template_content (str): The contents of the template file.
    Returns:
        dict: A dictionary of user-defined variables and their values.
    """
    # Use a regex pattern that allows for whitespace and special characters in variable names
    # This pattern matches anything between {{ and }} that's not a curly brace
    pattern = r'\{\{\s*([^{}]+?)\s*\}\}'
    user_vars = re.findall(pattern, template_content)
    user_inputs = {}
    
    for var in user_vars:
        # Strip whitespace from the variable name
        clean_var = var.strip()
        # Only prompt for non-empty variable names that haven't been prompted before
        if clean_var and clean_var not in user_inputs:
            user_inputs[clean_var] = prompt(f"Enter value for {clean_var}: ")
    
    return user_inputs

def process_template(template_content, files_data, user_inputs):
    """
    Process the Jinja2 template with the given data and user inputs.

    Args:
        template_content (str): The contents of the template file.
        files_data (list): List of processed file data.
        user_inputs (dict): Dictionary of user-defined variables and their values.

    Returns:
        str: The processed template content.
    """
    try:
        template = Template(template_content)
        return template.render(files=files_data, **user_inputs)
    except Exception as e:
        raise ValueError(f"Error processing template: {e}")
