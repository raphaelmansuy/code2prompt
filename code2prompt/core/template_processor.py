import os
from jinja2 import Environment
from jinja2 import TemplateNotFound
from code2prompt.utils.include_loader import CircularIncludeError, IncludeLoader
from code2prompt.utils.logging_utils import log_error
from prompt_toolkit import prompt
import re


def load_template(template_path):
    """
    Load a template file from the given path.

    Args:
        template_path (str): The path to the template file.

    Returns:
        str: The contents of the template file.

    Raises:
        IOError: If there is an error loading the template file.
    """
    try:
        with open(template_path, "r", encoding="utf-8") as file:
            return file.read()
    except IOError as e:
        raise IOError(f"Error loading template file: {e}") from e


def get_user_inputs(template_content):
    """
    Extracts user inputs from a template content.

    Args:
        template_content (str): The content of the template.

    Returns:
        dict: A dictionary containing the user inputs, where the keys are the variable names and the values are the user-entered values.
    """
    pattern = r"{{\s*input:([^{}]+?)\s*}}"
    matches = re.finditer(pattern, template_content)

    user_inputs = {}
    for match in matches:
        var_name = match.group(1).strip()
        if var_name and var_name not in user_inputs:
            user_inputs[var_name] = prompt(f"Enter value for {var_name}: ")

    return user_inputs


def replace_input_placeholders(template_content, user_inputs):
    """
    Replaces input placeholders in the template content with user inputs.

    Args:
        template_content (str): The content of the template.
        user_inputs (dict): A dictionary containing user inputs.

    Returns:
        str: The template content with input placeholders replaced by user inputs.
    """
    pattern = r"{{\s*input:([^{}]+?)\s*}}"

    def replace_func(match):
        var_name = match.group(1).strip()
        return user_inputs.get(var_name, "")

    return re.sub(pattern, replace_func, template_content)


def process_template(template_content, files_data, user_inputs, template_path):
    """
    Process a template by replacing input placeholders with user-provided values and rendering the template.

    Args:
        template_content (str): The content of the template to be processed.
        files_data (dict): A dictionary containing data for files that may be referenced in the template.
        user_inputs (dict): A dictionary containing user-provided values for input placeholders in the template.
        template_path (str): The path to the template file.

    Returns:
        str: The processed template content with input placeholders replaced and rendered.

    Raises:
        TemplateNotFound: If the template file is not found at the specified path.
        CircularIncludeError: If a circular include is detected in the template.
        Exception: If there is an error processing the template.

    """
    try:
        template_dir = os.path.dirname(template_path)
        env = Environment(
            loader=IncludeLoader(template_dir),
            autoescape=True,
            keep_trailing_newline=True,
        )
        # Replace input placeholders with user-provided values
        processed_content = replace_input_placeholders(template_content, user_inputs)
        template = env.from_string(processed_content)
        return template.render(files=files_data, **user_inputs)
    except TemplateNotFound as e:
        log_error(
            f"Template file not found: {e.name}. Please check the path and ensure the file exists."
        )
        return None
    except CircularIncludeError as e:
        log_error(f"Circular include detected: {str(e)}")
        return None
    except IOError as e:
        log_error(f"Error processing template: {e}")
        return None
