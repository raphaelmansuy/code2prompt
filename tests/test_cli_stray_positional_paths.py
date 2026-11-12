"""Regression tests for issue #25.

A shell expands an unquoted glob before click sees it, so
``code2prompt --path . --filter **.py`` can arrive as
``code2prompt --path . --filter core_rag.py utils.py ...``: the first
expanded filename is swallowed as the --filter value and the next one used
to be mistaken for a subcommand name ("No such command 'core_rag.py'").
Stray positional arguments that are existing files/directories are now
treated as extra input paths for `generate` instead of failing.
"""

import pytest
from click.testing import CliRunner

from code2prompt.main import cli


@pytest.fixture
def py_project(tmp_path, monkeypatch):
    """A tiny project with two .py files; tests run with it as cwd."""
    (tmp_path / "core_rag.py").write_text('print("hello")\n')
    (tmp_path / "utils.py").write_text("x = 1\n")
    monkeypatch.chdir(tmp_path)
    return tmp_path


def test_shell_expanded_glob_is_treated_as_extra_paths(py_project):
    """The exact argv a shell produces for unquoted --filter **.py."""
    runner = CliRunner()
    result = runner.invoke(
        cli,
        ["--path", ".", "--filter", "core_rag.py", "utils.py", "--output", "out.md"],
    )
    assert result.exit_code == 0, result.output
    output = (py_project / "out.md").read_text()
    assert "core_rag.py" in output
    assert "utils.py" in output
    assert "Treating unexpected argument(s)" in result.output


def test_bare_stray_file_without_path_option(py_project):
    runner = CliRunner()
    result = runner.invoke(cli, ["core_rag.py", "--output", "out.md"])
    assert result.exit_code == 0, result.output
    output = (py_project / "out.md").read_text()
    assert "core_rag.py" in output
    assert "utils.py" not in output


def test_same_file_via_path_and_stray_arg_is_not_duplicated(py_project):
    runner = CliRunner()
    result = runner.invoke(
        cli,
        ["--path", "core_rag.py", "core_rag.py", "--output", "out.md"],
    )
    assert result.exit_code == 0, result.output
    output = (py_project / "out.md").read_text()
    assert output.count("## File: core_rag.py") == 1


def test_unknown_non_path_word_still_errors(py_project):
    runner = CliRunner()
    result = runner.invoke(cli, ["genrate"])
    assert result.exit_code != 0
    assert "No such command 'genrate'" in result.output


def test_analyze_subcommand_still_works(py_project):
    runner = CliRunner()
    result = runner.invoke(cli, ["analyze", "--path", "."])
    assert result.exit_code == 0, result.output
    assert ".py: 2 files" in result.output


def test_generate_subcommand_still_works(py_project):
    runner = CliRunner()
    result = runner.invoke(cli, ["generate", "--path", ".", "--output", "out.md"])
    assert result.exit_code == 0, result.output
    output = (py_project / "out.md").read_text()
    assert "core_rag.py" in output
    assert "utils.py" in output
