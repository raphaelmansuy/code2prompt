from pathlib import Path


def create_templates_directory():
    """
    Create a 'templates' directory in the current working directory and
    populate it with example template files.
    """
    # Define the path for the templates directory
    templates_dir = Path.cwd() / "templates"

    # Create the templates directory if it doesn't exist
    templates_dir.mkdir(exist_ok=True)

    # Define example templates
    example_templates = {
        "basic.j2": """# Code Summary

{% for file in files %}
## {{ file.path }}

```{{ file.language }}
{{ file.content }}
```

{% endfor %}
""",
        "detailed.j2": """# Project Code Analysis

{% for file in files %}
## File: {{ file.path }}

- **Language**: {{ file.language }}
- **Size**: {{ file.size }} bytes
- **Last Modified**: {{ file.modified }}

### Code:

```{{ file.language }}
{{ file.content }}
```

### Analysis:
[Your analysis for {{ file.path }} goes here]

{% endfor %}
""",
        "custom.md": """# {{ project_name }}

{{ project_description }}

{% for file in files %}
## {{ file.path }}

{{ file_purpose }}

```{{ file.language }}
{{ file.content }}
```

{% endfor %}

## Next Steps:
{{ next_steps }}
""",
    }

    # Write example templates to files
    for filename, content in example_templates.items():
        file_path = templates_dir / filename
        with file_path.open("w") as f:
            f.write(content)

    print(f"Templates directory created at: {templates_dir}")
    print("Example templates added:")
    for filename, _ in example_templates.items():
        print(f"- {filename}")
