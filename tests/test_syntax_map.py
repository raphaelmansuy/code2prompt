"""syntax_map option validation: malformed entries must fail cleanly."""

from click.testing import CliRunner

from code2prompt.main import cli


def test_syntax_map_without_colon_is_rejected_cleanly():
    # Regression: '--syntax-map py' crashed with an unhandled ValueError
    # traceback ("not enough values to unpack") instead of a usage error.
    result = CliRunner().invoke(cli, ["--path", ".", "--syntax-map", "py"])
    assert result.exit_code == 2
    assert not isinstance(result.exception, ValueError)


def test_syntax_map_with_empty_parts_is_rejected_cleanly():
    result = CliRunner().invoke(cli, ["--path", ".", "--syntax-map", "py:"])
    assert result.exit_code == 2
    assert not isinstance(result.exception, ValueError)
