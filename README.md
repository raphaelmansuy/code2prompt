
# Code2Prompt

Code2Prompt is a powerful command-line tool that simplifies the process of providing context to Large Language Models (LLMs) by generating a comprehensive Markdown file containing the content of your codebase. 

With Code2Prompt, you can easily create a well-structured and informative document that serves as a valuable resource for feeding questions to LLMs, enabling them to better understand and assist with your code-related queries.

![](./docs/code2Prompt.jpg)

## Features

- Automatically traverses a directory and its subdirectories to include all relevant files
- Supports filtering files based on patterns (e.g., "*.py" to include only Python files)
- Respects .gitignore files to exclude unwanted files and directories
- Generates a table of contents with links to each file section
- Provides file metadata such as extension, size, creation time, and modification time
- Optionally strips comments from code files to focus on the core code
- Includes the actual code content of each file in fenced code blocks
- Handles binary files and files with encoding issues gracefully
- Supports custom Jinja2 templates for flexible output formatting
- Offers token counting functionality for generated prompts

## How It Works

The following diagram illustrates the high-level workflow of Code2Prompt:

Diagram

1. The tool starts by parsing the command-line options provided by the user.
2. It then parses the .gitignore file (if specified) to obtain a set of patterns for excluding files and directories.
3. The tool traverses the specified directory and its subdirectories, processing each file encountered.
4. For each file, it checks if the file is ignored based on the .gitignore patterns. If ignored, it skips the file and moves to the next one.
5. If the file is not ignored, it checks if the file matches the filter pattern (if provided). If the file doesn't match the filter, it skips the file and moves to the next one.
6. If the file matches the filter pattern, it checks if the file is a binary file. If it is, it skips the file and moves to the next one.
7. If the file is not a binary file, the tool extracts the file metadata (extension, size, creation time, modification time).
8. It then reads the file content and generates a file summary and code block.
9. The file summary, code block, and metadata are appended to the Markdown content.
10. Steps 4-9 are repeated for each file in the directory and its subdirectories.
11. After processing all files, the tool generates a table of contents based on the file paths.
12. If a custom template is provided, the tool processes the template with the collected data.
13. If token counting is enabled, the tool counts the tokens in the generated content.
14. If an output file is specified, the generated Markdown content is written to the file. Otherwise, it is printed to the console.
15. The tool ends its execution.

## Project Structure

The Code2Prompt project is organized as follows:

- `code2prompt/`: Main package directory
  - `__init__.py`: Package initialization
  - `main.py`: Entry point of the application
  - `process_file.py`: File processing logic
  - `template_processor.py`: Custom template processing
  - `write_output.py`: Output writing functionality
  - `utils/`: Utility functions
    - `add_line_numbers.py`: Function to add line numbers to code
    - `generate_markdown_content.py`: Markdown content generation
    - `is_binary.py`: Binary file detection
    - `is_filtered.py`: File filtering logic
    - `is_ignored.py`: Gitignore pattern matching
    - `language_inference.py`: Programming language inference
    - `parse_gitignore.py`: Gitignore file parsing
  - `comment_stripper/`: Comment removal functionality
    - `__init__.py`: Subpackage initialization
    - `strip_comments.py`: Main comment stripping logic
    - `c_style.py`: C-style comment removal
    - `html_style.py`: HTML-style comment removal
    - `python_style.py`: Python-style comment removal
    - `r_style.py`: R-style comment removal
    - `shell_style.py`: Shell-style comment removal
    - `sql_style.py`: SQL-style comment removal
    - `matlab_style.py`: MATLAB-style comment removal

## Installation

There are two ways to install Code2Prompt:

### Using Poetry

Code2Prompt is built using Poetry, a dependency management and packaging tool for Python. To install Code2Prompt using Poetry, follow these steps:

1. Make sure you have Poetry installed. If you don't have it installed, you can install it by running:
   ```
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. Clone the Code2Prompt repository:
   ```
   git clone https://github.com/raphael.mansuy/code2prompt.git
   ```

3. Navigate to the project directory:
   ```
   cd code2prompt
   ```

4. Install the dependencies using Poetry:
   ```
   poetry install
   ```

### Using pipx

Alternatively, you can install Code2Prompt using pipx, a tool for installing and running Python applications in isolated environments. To install Code2Prompt using pipx, follow these steps:

1. Make sure you have pipx installed. If you don't have it installed, you can install it by running:
   ```
   python3 -m pip install --user pipx
   python3 -m pipx ensurepath
   ```

2. Install Code2Prompt using pipx:
   ```
   pipx install git+https://github.com/raphaelmansuy/code2prompt.git
   ```

   This command will clone the Code2Prompt repository and install it in an isolated environment managed by pipx.

3. After installation, you can run Code2Prompt using the `code2prompt` command:
   ```
   code2prompt --path /path/to/your/codebase --output output.md
   ```

Using pipx provides a convenient way to install and run Code2Prompt without affecting your system-wide Python installation.

## Usage

To generate a Markdown file with the content of your codebase, use the following command:

```
code2prompt --path /path/to/your/codebase --output output.md
```

### Command-line Options

- `--path` or `-p` (required): Path to the directory containing your codebase.
- `--output` or `-o` (optional): Name of the output Markdown file. If not provided, the output will be displayed in the console.
- `--gitignore` or `-g` (optional): Path to a custom .gitignore file. If not provided, the tool will look for a .gitignore file in the specified directory.
- `--filter` or `-f` (optional): Comma-separated filter patterns to include specific files (e.g., "*.py,*.js" to include only Python and JavaScript files).
- `--exclude` or `-e` (optional): Comma-separated patterns to exclude files (e.g., "*.txt,*.md" to exclude text and Markdown files).
- `--case-sensitive` (optional): Perform case-sensitive pattern matching.
- `--suppress-comments` or `-s` (optional): Strip comments from the code files. If not provided, comments will be included.
- `--line-number` or `-ln` (optional): Add line numbers to source code blocks.
- `--no-codeblock` (optional): Disable wrapping code inside markdown code blocks.
- `--template` or `-t` (optional): Path to a Jinja2 template file for custom prompt generation.
- `--tokens` (optional): Display the token count of the generated prompt.
- `--encoding` (optional): Specify the tokenizer encoding to use (default: 'cl100k_base').

### Examples

1. Generate a Markdown file for a Python project:
   ```
   code2prompt --path /path/to/your/python/project --output python_project.md --filter "*.py"
   ```

2. Generate a Markdown file for a web development project:
   ```
   code2prompt --path /path/to/your/web/project --output web_project.md --filter "*.js,*.html,*.css"
   ```

3. Generate a Markdown file for a project with a custom .gitignore file:
   ```
   code2prompt --path /path/to/your/project --output project.md --gitignore /path/to/custom/.gitignore
   ```

4. Generate a Markdown file with comments stripped from code files:
   ```
   code2prompt --path /path/to/your/project --output project.md --suppress-comments
   ```

5. Generate a Markdown file using a custom template:
   ```
   code2prompt --path /path/to/your/project --output project.md --template /path/to/custom/template.jinja2
   ```

6. Generate a Markdown file and display token count:
   ```
   code2prompt --path /path/to/your/project --output project.md --tokens
   ```

## Templating System

Code2Prompt includes a powerful templating system that allows you to customize the output format using Jinja2 templates. This feature provides flexibility in generating prompts tailored to specific use cases or LLM requirements.

### How It Works

1. **Template Loading**: When you specify a template file using the `--template` option, Code2Prompt loads the Jinja2 template from the specified file.

2. **Variable Extraction**: The system extracts user-defined variables from the template. These are placeholders in the template that you want to fill with custom values.

3. **User Input**: For each extracted variable, Code2Prompt prompts the user to enter a value.

4. **Data Preparation**: The system prepares a context dictionary containing:
   - `files`: A list of dictionaries, each representing a processed file with its metadata and content.
   - User-defined variables and their input values.

5. **Template Rendering**: The Jinja2 template is rendered using the prepared context, producing the final output.

### Example

Let's say you have a template file named `custom_prompt.jinja2` with the following content:

```jinja2
You are a {{ role }} tasked with analyzing the following codebase:

{% for file in files %}
## File: {{ file.path }}
Language: {{ file.language }}
Content:
{{ file.language }}
{{ file.content }}

{% endfor %}

Based on this codebase, please {{ task }}.
```

You can use this template with Code2Prompt as follows:

```bash
code2prompt --path /path/to/your/project --template custom_prompt.jinja2
```

When you run this command, Code2Prompt will:

1. Load the `custom_prompt.jinja2` template.
2. Detect the user-defined variables: `role` and `task`.
3. Prompt you to enter values for these variables:
   ```
   Enter value for role: senior software engineer
   Enter value for task: identify potential security vulnerabilities
   ```
4. Process the files in the specified path.
5. Render the template with the file data and user inputs.

The resulting output might look like this:

```
You are a senior software engineer tasked with analyzing the following codebase:

## File: /path/to/your/project/main.py
Language: python
Content:
```python
import os

def read_sensitive_file(filename):
    with open(filename, 'r') as f:
        return f.read()

secret = read_sensitive_file('secret.txt')
print(f"The secret is: {secret}")


## File: /path/to/your/project/utils.py
Language: python
Content:
```python
import base64

def encode_data(data):
    return base64.b64encode(data.encode()).decode()

def decode_data(encoded_data):
    return base64.b64decode(encoded_data).decode()


Based on this codebase, please identify potential security vulnerabilities.
```

This templating system allows you to create custom prompts that can be easily adapted for different analysis tasks, code review scenarios, or any other purpose where you need to present code to an LLM in a structured format.


## Build

To build a distributable package of Code2Prompt using Poetry, follow these steps:

1. Make sure you are in the project directory.

2. Run the following command to build the package:
   ```
   poetry build
   ```

   This command will create a distributable package in the `dist` directory.

3. You can then install the package using pip:
   ```
   pip install dist/code2prompt-<version>.tar.gz
   ```

   Replace `<version>` with the actual version number of the package.

## License

Code2Prompt is released under the MIT License. See [LICENSE](./LICENCE.md) for more information.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request on the [GitHub repository](https://github.com/raphaelmansuy/code2prompt).

## Acknowledgements

Code2Prompt was inspired by the need to provide better context to LLMs when asking code-related questions. We would like to thank the open-source community for their valuable contributions.

If you have any questions or need further assistance, please don't hesitate to reach out. Happy coding!

Made with ❤️ by Raphël MANSUY
