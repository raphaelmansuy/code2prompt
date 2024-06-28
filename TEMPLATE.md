
# Using the Templating System in code2prompt

The templating system in `code2prompt` allows you to create custom output formats using Jinja2 templates. This feature is activated by using the `--template` or `-t` option when running the tool.

## Basic Usage

```bash
code2prompt generate --path path/to/codebase --template path/to/template.j2 --output output.md
```

## Available Variables

In your Jinja2 template, you have access to the following variables:

1. `files`: A list of dictionaries, where each dictionary contains information about a processed file. Each file dictionary includes:
   - `path`: The file path (string)
   - `extension`: The file extension (string)
   - `language`: The inferred programming language (string)
   - `size`: The file size in bytes (integer)
   - `created`: The file creation timestamp (string)
   - `modified`: The file modification timestamp (string)
   - `content`: The file content (string)
   - `no_codeblock`: A flag indicating whether to disable wrapping code inside markdown code blocks (boolean)

2. User-defined variables: Any additional variables you define in your template using `{{ variable_name }}` syntax will be prompted for input when running the tool.

## Template Examples

### Example 1: Basic File Listing

```jinja2
# Code Analysis Report

{% for file in files %}
## {{ file.path }}

- Language: {{ file.language }}
- Size: {{ file.size }} bytes
- Last modified: {{ file.modified }}

```{{ file.language }}
{{ file.content }}
```

{% endfor %}
```

### Example 2: Custom Project Overview

```jinja2
# {{ project_name }} Analysis

Project: {{ project_name }}
Analyzed on: {{ analysis_date }}

## File Summary

Total files analyzed: {{ files|length }}

{% for file in files %}
- {{ file.path }} ({{ file.language }}, {{ file.size }} bytes)
{% endfor %}

## Detailed Code Review

{% for file in files %}
### {{ file.path }}

```{{ file.language }}
{{ file.content }}
```

{% endfor %}
```

In this example, `project_name` and `analysis_date` are user-defined variables. When you run the tool with this template, it will prompt you to enter values for these variables.

### Example 3: Language-specific Analysis

```jinja2
# {{ project_name }} Code Analysis

{% set python_files = files|selectattr("language", "equalto", "python")|list %}
{% set js_files = files|selectattr("language", "equalto", "javascript")|list %}

## Python Files ({{ python_files|length }})

{% for file in python_files %}
### {{ file.path }}

```python
{{ file.content }}
```

{% endfor %}

## JavaScript Files ({{ js_files|length }})

{% for file in js_files %}
### {{ file.path }}

```javascript
{{ file.content }}
```

{% endfor %}
```

This template groups files by language and creates separate sections for Python and JavaScript files.

## Tips for Using Templates

1. Use Jinja2 control structures like `{% for %}`, `{% if %}`, etc., to customize the output format.
2. Utilize Jinja2 filters to manipulate data, e.g., `{{ variable|upper }}` to convert text to uppercase.
3. Create user-defined variables for dynamic content that you want to input at runtime.
4. Use the `files` list to iterate over all processed files and access their properties.
5. Remember that the `content` of each file is already processed according to the command-line options (e.g., comments stripped if `--suppress-comments` was used).
