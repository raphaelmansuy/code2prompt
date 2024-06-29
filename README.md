# Code2Prompt

Code2Prompt is a powerful command-line tool that generates comprehensive prompts from codebases, designed to streamline interactions between developers and Large Language Models (LLMs) for code analysis, documentation, and improvement tasks.

[![PyPI version](https://badge.fury.io/py/code2prompt.svg)](https://badge.fury.io/py/code2prompt)

![](./docs/code2Prompt.jpg)


## Table of Contents

1. [Why Code2Prompt?](#why-code2prompt)
2. [Features](#features)
3. [Installation](#installation)
4. [Quick Start](#quick-start)
5. [Usage](#usage)
6. [Options](#options)
7. [Examples](#examples)
8. [Templating System](#templating-system)
9. [Integration with LLM CLI](#integration-with-llm-cli)
10. [GitHub Actions Integration](#github-actions-integration)
11. [Troubleshooting](#troubleshooting)
12. [Contributing](#contributing)
13. [License](#license)

## Why Code2Prompt?

When working with Large Language Models on software development tasks, providing extensive context about the codebase is crucial. Code2Prompt addresses this need by:

- Offering a holistic view of your project, enabling LLMs to better understand the overall structure and dependencies.
- Allowing for more accurate recommendations and suggestions from LLMs.
- Maintaining consistency in coding style and conventions across the project.
- Facilitating better interdependency analysis and refactoring suggestions.
- Enabling more contextually relevant documentation generation.
- Helping LLMs learn and apply project-specific patterns and idioms.

By generating a comprehensive Markdown file containing the content of your codebase, Code2Prompt simplifies the process of providing context to LLMs, making it an invaluable tool for developers working with AI-assisted coding tools.

## Features

- Process single files or entire directories
- Support for multiple programming languages
- Gitignore integration
- Comment stripping
- Line number addition
- Custom output formatting using Jinja2 templates
- Token counting for AI model compatibility
- Clipboard copying of generated content
- Automatic traversal of directories and subdirectories
- File filtering based on patterns
- File metadata inclusion (extension, size, creation time, modification time)
- Graceful handling of binary files and encoding issues

## Installation

Choose one of the following methods to install Code2Prompt:

### Using pip (recommended)

```bash
pip install code2prompt
```

### Using Poetry

1. Ensure you have Poetry installed:
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. Install Code2Prompt:
   ```bash
   poetry add code2prompt
   ```

### Using pipx

```bash
pipx install code2prompt
```

## Quick Start

1. Generate a prompt from a single Python file:
   ```bash
   code2prompt --path /path/to/your/script.py
   ```

2. Process an entire project directory and save the output:
   ```bash
   code2prompt --path /path/to/your/project --output project_summary.md
   ```

3. Generate a prompt for multiple files, excluding tests:
   ```bash
   code2prompt --path /path/to/src --path /path/to/lib --exclude "*/tests/*" --output codebase_summary.md
   ```

## Usage

The basic syntax for Code2Prompt is:

```bash
code2prompt --path /path/to/your/code [OPTIONS]
```

For multiple paths:

```bash
code2prompt --path /path/to/dir1 --path /path/to/file2.py [OPTIONS]
```

## Options

| Option | Short | Description |
|--------|-------|-------------|
| `--path` | `-p` | Path(s) to the directory or file to process (required, multiple allowed) |
| `--output` | `-o` | Name of the output Markdown file |
| `--gitignore` | `-g` | Path to the .gitignore file |
| `--filter` | `-f` | Comma-separated filter patterns to include files (e.g., "*.py,*.js") |
| `--exclude` | `-e` | Comma-separated patterns to exclude files (e.g., "*.txt,*.md") |
| `--case-sensitive` | | Perform case-sensitive pattern matching |
| `--suppress-comments` | `-s` | Strip comments from the code files |
| `--line-number` | `-ln` | Add line numbers to source code blocks |
| `--no-codeblock` | | Disable wrapping code inside markdown code blocks |
| `--template` | `-t` | Path to a Jinja2 template file for custom prompt generation |
| `--tokens` | | Display the token count of the generated prompt |
| `--encoding` | | Specify the tokenizer encoding to use (default: "cl100k_base") |
| `--create-templates` | | Create a templates directory with example templates |
| `--version` | `-v` | Show the version and exit |

## Examples

1. Generate documentation for a Python library:
   ```bash
   code2prompt --path /path/to/library --output library_docs.md --suppress-comments --line-number --filter "*.py"
   ```

2. Prepare a codebase summary for a code review, focusing on JavaScript and TypeScript files:
   ```bash
   code2prompt --path /path/to/project --filter "*.js,*.ts" --exclude "node_modules/*,dist/*" --template code_review.j2 --output code_review.md
   ```

3. Create input for an AI model to suggest improvements, focusing on a specific directory:
   ```bash
   code2prompt --path /path/to/src/components --suppress-comments --tokens --encoding cl100k_base --output ai_input.md
   ```

4. Analyze comment density across a multi-language project:
   ```bash
   code2prompt --path /path/to/project --template comment_density.j2 --output comment_analysis.md --filter "*.py,*.js,*.java"
   ```

5. Generate a prompt for a specific set of files, adding line numbers:
   ```bash
   code2prompt --path /path/to/important_file1.py --path /path/to/important_file2.js --line-number --output critical_files.md
   ```

## Templating System

Code2Prompt supports custom output formatting using Jinja2 templates. 

To use a custom template:

```bash
code2prompt --path /path/to/code --template /path/to/your/template.j2
```

Example custom template (code_review.j2):

```jinja2
# Code Review Summary

{% for file in files %}
## {{ file.path }}

- **Language**: {{ file.language }}
- **Size**: {{ file.size }} bytes
- **Last Modified**: {{ file.modified }}

### Code:

```{{ file.language }}
{{ file.content }}
```

### Review Notes:

- [ ] Check for proper error handling
- [ ] Verify function documentation
- [ ] Look for potential performance improvements

{% endfor %}

## Overall Project Health:

- Total files reviewed: {{ files|length }}
- Primary languages: [List top 3 languages]
- Areas for improvement: [Add your observations]
```

## Templating system documentation

A full documentation of the templating system is available at [Documentation Templating](./TEMPLATE.md)

## Integration with LLM CLI

Code2Prompt can be seamlessly integrated with Simon Willison's [llm](https://github.com/simonw/llm) CLI tool to leverage the power of large language models for code analysis and improvement.

### Installation

First, ensure you have both Code2Prompt and llm installed:

```bash
pip install code2prompt llm
```

### Basic Usage

1. Generate a code summary and analyze it with an LLM:
   ```bash
   code2prompt --path /path/to/your/project | llm "Analyze this codebase and provide insights on its structure and potential improvements"
   ```

2. Process a specific file and get refactoring suggestions:
   ```bash
   code2prompt --path /path/to/your/script.py | llm "Suggest refactoring improvements for this code"
   ```

### Advanced Use Cases

1. Code Review Assistant:
   ```bash
   code2prompt --path /path/to/project --filter "*.py" | llm "Perform a code review on this Python project. Identify potential bugs, suggest improvements for code quality, and highlight any security concerns."
   ```

2. Documentation Generator:
   ```bash
   code2prompt --path /path/to/project --suppress-comments | llm "Generate detailed documentation for this project. Include an overview of the project structure, main components, and how they interact. Provide examples of how to use key functions and classes."
   ```

3. Refactoring Suggestions:
   ```bash
   code2prompt --path /path/to/complex_module.py | llm "Analyze this Python module and suggest refactoring opportunities. Focus on improving readability, reducing complexity, and enhancing maintainability."
   ```

## GitHub Actions Integration

You can integrate Code2Prompt and llm into your GitHub Actions workflow to automatically analyze your codebase on every push. Here's an example workflow:

```yaml
name: Code Analysis
on: [push]
jobs:
  analyze-code:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.x'
    - name: Install dependencies
      run: |
        pip install code2prompt llm
    - name: Analyze codebase
      run: |
        code2prompt --path . | llm "Perform a comprehensive analysis of this codebase. Identify areas for improvement, potential bugs, and suggest optimizations." > analysis.md
    - name: Upload analysis
      uses: actions/upload-artifact@v2
      with:
        name: code-analysis
        path: analysis.md
```

This workflow will generate a code analysis report on every push to your repository.

## Troubleshooting

1. **Issue**: Code2Prompt is not recognizing my .gitignore file.
   **Solution**: Ensure you're running Code2Prompt from the root of your project, or specify the path to your .gitignore file using the `--gitignore` option.

2. **Issue**: The generated output is too large for my AI model.
   **Solution**: Use the `--tokens` option to check the token count, and consider using more specific `--filter` or `--exclude` options to reduce the amount of processed code.


3. **Issue**: Encoding-related errors when processing files.
   **Solution**: Try specifying a different encoding with the `--encoding` option, e.g., `--encoding utf-8`.

4. **Issue**: Some files are not being processed.
   **Solution**: Check if the files are binary or if they match any exclusion patterns. Use the `--case-sensitive` option if your patterns are case-sensitive.

## Contributing

Contributions to Code2Prompt are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

Code2Prompt is released under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Made with ❤️ by Raphaël MANSUY

This comprehensive README provides a detailed guide to using Code2Prompt, including its features, installation methods, usage examples, and integration with other tools like llm and GitHub Actions. It addresses various use cases and provides troubleshooting tips to help users get the most out of the tool.

