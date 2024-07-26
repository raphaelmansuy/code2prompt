from typing import OrderedDict, Tuple, List
import os
from jinja2 import Environment, FileSystemLoader
from code2prompt.utils.include_loader import CircularIncludeError, IncludeLoader
from prompt_toolkit import prompt
import re

def load_template(template_path):
    """
    Load a Jinja2 template from a file.
    """
    try:
        with open(template_path, 'r', encoding='utf-8') as file:
            return file.read()
    except IOError as e:
        raise IOError(f"Error loading template file: {e}") from e

def get_user_inputs(template_content: str) -> Tuple[OrderedDict[str, str], List[Tuple[int, int, str]]]:
    """
    Extract user-defined variables from the template and prompt for input.
    Returns a tuple of user inputs and variable positions.
    """
    # Use a regex pattern that excludes Jinja execute blocks and matches the new input syntax
    pattern = r'{{\s*input:([^{}]+?)\s*}}'
    matches = list(re.finditer(pattern, template_content))
    
    user_inputs = OrderedDict()
    positions = []
    
    for match in matches:
        var_name = match.group(1).strip()
        positions.append((match.start(), match.end(), var_name))
        
        # Only prompt for non-empty variable names that haven't been prompted before
        if var_name and var_name not in user_inputs:
            user_inputs[var_name] = prompt(f"Enter value for {var_name}: ")
    
    return user_inputs, positions

def process_template(template_content, files_data, user_inputs, template_path):
    try:
        template_dir = os.path.dirname(template_path)
        env = Environment(
            loader=IncludeLoader(template_dir),
            autoescape=True,
            keep_trailing_newline=True
        )
        
        # Get user inputs and variable positions
        user_inputs, positions = get_user_inputs(template_content)
        
        # Replace input placeholders with user-provided values
        for start, end, var_name in reversed(positions):
            replacement = user_inputs.get(var_name, '')
            template_content = template_content[:start] + replacement + template_content[end:]
        
        template = env.from_string(template_content)
        return template.render(files=files_data, **user_inputs)
    except CircularIncludeError as e:
        raise ValueError(f"Circular include detected: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error processing template: {e}")