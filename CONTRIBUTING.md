# Contributing to code2prompt

Thank you for your interest in contributing to code2prompt! We welcome contributions from the community to help improve and grow this project. This document outlines the process for contributing and provides guidelines to ensure a smooth collaboration.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Development Setup](#development-setup)
3. [Making Changes](#making-changes)
4. [Submitting Changes](#submitting-changes)
5. [Coding Standards](#coding-standards)
6. [Running Tests](#running-tests)
7. [Reporting Issues](#reporting-issues)
8. [Community Guidelines](#community-guidelines)

## Getting Started

Before you begin:

1. Ensure you have a [GitHub account](https://github.com/signup).
2. Familiarize yourself with the [code2prompt documentation](https://github.com/raphaelmansuy/code2prompt#readme).
3. Check the [issues page](https://github.com/raphaelmansuy/code2prompt/issues) for existing issues or feature requests.

## Development Setup

To set up your development environment:

1. Fork the repository on GitHub.
2. Clone your fork locally:
   ```
   git clone https://github.com/your-username/code2prompt.git
   cd code2prompt
   ```
3. Ensure you have Python 3.7+ and [Poetry](https://python-poetry.org/docs/#installation) installed.
4. Install dependencies using Poetry:
   ```
   poetry install
   ```
5. Activate the virtual environment:
   ```
   poetry shell
   ```

## Making Changes

1. Create a new branch for your changes:
   ```
   git checkout -b feature/your-feature-name
   ```
2. Make your changes and commit them with a clear, descriptive commit message.
3. Add or update tests as necessary.
4. Update documentation if you're changing functionality.

## Submitting Changes

1. Push your changes to your fork:
   ```
   git push origin feature/your-feature-name
   ```
2. Submit a pull request to the main repository.
3. Ensure your PR description clearly describes the problem and solution.
4. Link any relevant issues in the PR description.

## Coding Standards

Please adhere to the following coding standards:

1. Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide for Python code.
2. Use meaningful variable and function names.
3. Write clear, concise comments and docstrings.
4. Ensure your code is compatible with Python 3.7+.
5. Use type hints where appropriate.

## Running Tests

Before submitting your changes, make sure all tests pass:

```
poetry run pytest
```

If you've added new functionality, please include appropriate tests.

## Reporting Issues

When reporting issues:

1. Use the [issue tracker](https://github.com/raphaelmansuy/code2prompt/issues).
2. Provide a clear, concise description of the issue.
3. Include steps to reproduce the problem.
4. Specify your operating system, Python version, and code2prompt version.
5. If possible, provide a minimal code example that demonstrates the issue.

## Community Guidelines

To ensure a positive and inclusive community:

1. Be respectful and considerate in your interactions.
2. Provide constructive feedback.
3. Avoid offensive or discriminatory language.
4. Help others when you can.
5. Follow the [Code of Conduct](CODE_OF_CONDUCT.md).

Thank you for contributing to code2prompt! Your efforts help make this project better for everyone.
