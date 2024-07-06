# Code2Prompt

[![PyPI version](https://badge.fury.io/py/code2prompt.svg)](https://badge.fury.io/py/code2prompt)

[![GitHub Stars](https://img.shields.io/github/stars/raphaelmansuy/code2prompt.svg)](https://github.com/raphaelmansuy/code2prompt/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/raphaelmansuy/code2prompt.svg)](https://github.com/raphaelmansuy/code2prompt/network/members)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Code2Prompt is a powerful command-line tool that generates comprehensive prompts from codebases, designed to streamline interactions between developers and Large Language Models (LLMs) for code analysis, documentation, and improvement tasks.


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
11. [Configuration File](#configuration-file)
12. [Troubleshooting](#troubleshooting)
13. [Contributing](#contributing)
14. [License](#license)

# Code2Prompt: Transform Your Codebase into AI-Ready Prompts

[![PyPI version](https://badge.fury.io/py/code2prompt.svg)](https://badge.fury.io/py/code2prompt)
[![GitHub Stars](https://img.shields.io/github/stars/raphaelmansuy/code2prompt.svg)](https://github.com/raphaelmansuy/code2prompt/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

![](./docs/screen-example1.png)

## Supercharge Your AI-Assisted Development

Code2Prompt is a powerful, open-source command-line tool that bridges the gap between your codebase and Large Language Models (LLMs). By converting your entire project into a comprehensive, AI-friendly prompt, Code2Prompt enables you to leverage the full potential of AI for code analysis, documentation, and improvement tasks.

### 🚀 Key Features

- **Holistic Codebase Representation**: Generate a well-structured Markdown prompt that captures your entire project's essence.
- **Intelligent Source Tree Generation**: Create a clear, hierarchical view of your codebase structure.
- **Customizable Prompt Templates**: Tailor your output using Jinja2 templates to suit specific AI tasks.
- **Smart Token Management**: Count and optimize tokens to ensure compatibility with various LLM token limits.
- **Gitignore Integration**: Respect your project's .gitignore rules for accurate representation.
- **Flexible File Handling**: Filter and exclude files using powerful glob patterns.
- **Clipboard Ready**: Instantly copy generated prompts to your clipboard for quick AI interactions.
- **Multiple Output Options**: Save to file or display in the console.
- **Enhanced Code Readability**: Add line numbers to source code blocks for precise referencing.

### 💡 Why Code2Prompt?

- **Contextual Understanding**: Provide LLMs with a comprehensive view of your project for more accurate suggestions and analysis.
- **Consistency Boost**: Maintain coding style and conventions across your entire project.
- **Efficient Refactoring**: Enable better interdependency analysis and smarter refactoring recommendations.
- **Improved Documentation**: Generate contextually relevant documentation that truly reflects your codebase.
- **Pattern Recognition**: Help LLMs learn and apply your project-specific patterns and idioms.

Transform the way you interact with AI for software development. With Code2Prompt, harness the full power of your codebase in every AI conversation.

Ready to elevate your AI-assisted development? Let's dive in! 🏊‍♂️

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


## Command Parameters

### `--filter` or `-f` and `--exclude` or `-e`

The `--filter` and `--exclude` options allow you to specify patterns for files or directories that should be included in or excluded from processing, respectively.

#### Syntax:
```
--filter "PATTERN1,PATTERN2,..."
--exclude "PATTERN1,PATTERN2,..."
```
or
```
-f "PATTERN1,PATTERN2,..."
-e "PATTERN1,PATTERN2,..."
```

#### Description:
- Both options accept a comma-separated list of patterns.
- Patterns can include wildcards (`*`) and directory indicators (`**`).
- Case-sensitive by default (use `--case-sensitive` flag to change this behavior).
- `--exclude` patterns take precedence over `--filter` patterns.

#### Examples:

1. Include only Python files:
   ```
   --filter "**.py"
   ```

2. Exclude all Markdown files:
   ```
   --exclude "**.md"
   ```

3. Include specific file types in the src directory:
   ```
   --filter "src/**.{js,ts}"
   ```

4. Exclude multiple file types and a specific directory:
   ```
   --exclude "**.log,**.tmp,**/node_modules/**"
   ```

5. Include all files except those in 'test' directories:
   ```
   --filter "**" --exclude "**/test/**"
   ```

6. Complex filtering (include JavaScript files, exclude minified and test files):
   ```
   --filter "**.js" --exclude "**.min.js,**test**.js"
   ```

7. Include specific files across all directories:
   ```
   --filter "**/config.json,**/README.md"
   ```

8. Exclude temporary files and directories:
   ```
   --exclude "**/.cache/**,**/tmp/**,**.tmp"
   ```

9. Include source files but exclude build output:
   ```
   --filter "src/**/*.{js,ts}" --exclude "**/dist/**,**/build/**"
   ```

10. Exclude version control and IDE-specific files:
    ```
    --exclude "**/.git/**,**/.vscode/**,**/.idea/**"
    ```

#### Important Notes:

- Always use double quotes around patterns to prevent shell interpretation of special characters.
- Patterns are matched against the full path of each file, relative to the project root.
- The `**` wildcard matches any number of directories.
- Single `*` matches any characters within a single directory or filename.
- Use commas to separate multiple patterns within the same option.
- Combine `--filter` and `--exclude` for fine-grained control over which files are processed.

#### Best Practices:

1. Start with broader patterns and refine as needed.
2. Test your patterns on a small subset of your project first.
3. Use the `--case-sensitive` flag if you need to distinguish between similarly named files with different cases.
4. When working with complex projects, consider using a configuration file to manage your filter and exclude patterns.

By using the `--filter` and `--exclude` options effectively and safely (with proper quoting), you can precisely control which files are processed in your project, ensuring both accuracy and security in your command execution.


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

Code2Prompt supports custom output formatting using Jinja2 templates. To use a custom template:

```bash
code2prompt --path /path/to/code --template /path/to/your/template.j2
```

### Creating Template Examples

Use the `--create-templates` command to generate example templates:

```bash
code2prompt --create-templates
```

This creates a `templates` directory with sample Jinja2 templates, including:

- [default.j2](./code2prompt//templates/default.j2): A general-purpose template
- [analyze-code.j2](./code2prompt/templates/analyze-code.j2): For detailed code analysis
- [code-review.j2](./code2prompt/templates/code-review.j2): For thorough code reviews
- [create-readme.j2](./code2prompt/templates/create-readme.j2): To assist in generating README files
- [improve-this-prompt.j2](./code2prompt/templates/improve-this-prompt.j2): For refining AI prompts

For full template documentation, see [Documentation Templating](./TEMPLATE.md).

## Integration with LLM CLI

Code2Prompt can be integrated with Simon Willison's [llm](https://github.com/simonw/llm) CLI tool for enhanced code analysis.

### Installation

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

For more advanced use cases, refer to the [Integration with LLM CLI](#integration-with-llm-cli) section in the full documentation.

## GitHub Actions Integration

You can integrate Code2Prompt into your GitHub Actions workflow. Here's an example:

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

## Understanding Tokens and Token Types in Code2Prompt

Tokens are the basic units of text that language models process. They can be words, parts of words, or even punctuation marks. Different tokenizer encodings split text into tokens in various ways. Code2Prompt supports multiple token types through its `--encoding` option, with "cl100k_base" as the default. This encoding, used by models like GPT-3.5 and GPT-4, is adept at handling code and technical content. Other common encodings include "p50k_base" (used by earlier GPT-3 models) and "r50k_base" (used by models like CodeX).

To count tokens in your generated prompt, use the `--tokens` flag:

```bash
code2prompt --path /your/project --tokens
```

For a specific encoding:

```bash
code2prompt --path /your/project --tokens --encoding p50k_base
```

Understanding token counts is crucial when working with AI models that have token limits, ensuring your prompts fit within the model's context window.


## Configuration File

Code2Prompt supports a `.code2promptrc` configuration file in JSON format for setting default options. Place this file in your project or home directory.

Example `.code2promptrc`:

```json
{
  "suppress_comments": true,
  "line_number": true,
  "encoding": "cl100k_base",
  "filter": "*.py,*.js",
  "exclude": "tests/*,docs/*"
}
```

## Troubleshooting

1. **Issue**: Code2Prompt is not recognizing my .gitignore file.
   **Solution**: Run Code2Prompt from the project root, or specify the .gitignore path with `--gitignore`.

2. **Issue**: The generated output is too large for my AI model.
   **Solution**: Use `--tokens` to check the count, and refine `--filter` or `--exclude` options.

3. **Issue**: Encoding-related errors when processing files.
   **Solution**: Try a different encoding with `--encoding`, e.g., `--encoding utf-8`.

4. **Issue**: Some files are not being processed.
   **Solution**: Check for binary files or exclusion patterns. Use `--case-sensitive` if needed.

## Contributing

Contributions to Code2Prompt are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

Code2Prompt is released under the MIT License. See the [LICENSE](LICENSE) file for details.

---

⭐ If you find Code2Prompt useful, please give us a star on GitHub! It helps us reach more developers and improve the tool. ⭐

## Project Growth
[![Star History Chart](https://api.star-history.com/svg?repos=raphaelmansuy/code2prompt&type=Date)](https://star-history.com/#raphaelmansuy/code2prompt&Date)

Made with ❤️ by Raphaël MANSUY