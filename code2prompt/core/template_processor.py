from typing import OrderedDict
import os
from jinja2 import Environment, FileSystemLoader
from code2prompt.utils.include_loader import CircularIncludeError, IncludeLoader
from prompt_toolkit import prompt
import re

def load_template(template_path):
    try:
        with open(template_path, 'r', encoding='utf-8') as file:
            return file.read()
    except IOError as e:
        raise IOError(f"Error loading template file: {e}") from e

def get_user_inputs(template_content):
    pattern = r'{{\s*input:([^{}]+?)\s*}}'
    matches = re.finditer(pattern, template_content)
    
    user_inputs = {}
    for match in matches:
        var_name = match.group(1).strip()
        if var_name and var_name not in user_inputs:
            user_inputs[var_name] = prompt(f"Enter value for {var_name}: ")
    
    return user_inputs

def replace_input_placeholders(template_content, user_inputs):
    pattern = r'{{\s*input:([^{}]+?)\s*}}'
    
    def replace_func(match):
        var_name = match.group(1).strip()
        return user_inputs.get(var_name, '')
    
    return re.sub(pattern, replace_func, template_content)

def process_template(template_content, files_data, user_inputs, template_path):
    try:
        template_dir = os.path.dirname(template_path)
        env = Environment(
            loader=IncludeLoader(template_dir),
            autoescape=True,
            keep_trailing_newline=True
        )
        
        # Replace input placeholders with user-provided values
        processed_content = replace_input_placeholders(template_content, user_inputs)
        
        template = env.from_string(processed_content)
        return template.render(files=files_data, **user_inputs)
    except CircularIncludeError as e:
        raise ValueError(f"Circular include detected: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error processing template: {e}")