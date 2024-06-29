# code2prompt/config.py
import json
from pathlib import Path

def load_config(current_dir):
    """
    Load configuration from .code2promptrc files.
    Searches in the current directory and all parent directories up to the home directory.
    """
    config = {}
    current_path = Path(current_dir).resolve()
    home_path = Path.home()
    while current_path >= home_path:
        rc_file = current_path / '.code2promptrc'
        if rc_file.is_file():
            with open(rc_file, 'r', encoding='utf-8') as f:
                file_config = json.load(f)
                if 'path' in file_config and isinstance(file_config['path'], str):
                    file_config['path'] = file_config['path'].split(',')
                config.update(file_config)
        if current_path == home_path:
            break
        current_path = current_path.parent
    return config

def merge_options(cli_options: dict, config_options: dict, default_options: dict) -> dict:
    """
    Merge CLI options, config options, and default options.
    CLI options take precedence over config options, which take precedence over default options.
    """
    merged = default_options.copy()
    
    # Update with config options
    for key, value in config_options.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = merge_options({}, value, merged[key])
        else:
            merged[key] = value
    
    # Update with CLI options, but only if they're different from the default
    for key, value in cli_options.items():
        if value != default_options.get(key):
            if isinstance(value, dict) and isinstance(merged.get(key), dict):
                merged[key] = merge_options(value, {}, merged[key])
            else:
                merged[key] = value
    
    # Special handling for 'path'
    if not merged['path'] and 'path' in config_options:
        merged['path'] = config_options['path']
    
    return merged