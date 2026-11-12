"""Regression tests for issue #26.

`--exclude "node_modules/**"` used to recurse into the excluded directory
and skip its files one by one (visible with `--log-level DEBUG`).
`retrieve_file_paths` now prunes such directories during traversal, so
their contents are never visited. Pruning is probed through the same
`is_filtered()` matcher used for files, so the returned file set is
unchanged — only the traversal skips the excluded subtree.
"""

import pytest
from pathlib import Path

import code2prompt.core.file_path_retriever as retriever
from code2prompt.core.file_path_retriever import (
    _iter_tree,
    is_excluded_directory,
    retrieve_file_paths,
)


@pytest.fixture
def project(tmp_path):
    """src/app.js + package.json, plus a big excluded node_modules tree."""
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "app.js").write_text('console.log("app");\n')
    (tmp_path / "package.json").write_text('{"name":"x"}\n')
    node_modules = tmp_path / "node_modules"
    (node_modules / "@scope" / "pkg" / "deep").mkdir(parents=True)
    for i in range(50):
        (node_modules / f"pkg{i}.js").write_text(f"// {i}\n")
        (node_modules / "@scope" / "pkg" / "deep" / f"f{i}.js").write_text(
            f"// deep {i}\n"
        )
    return tmp_path


def _visited_paths(monkeypatch):
    """Record every path should_process_file is called with."""
    seen = []
    real = retriever.should_process_file

    def recording(*args, **kwargs):
        seen.append(args[0])
        return real(*args, **kwargs)

    monkeypatch.setattr(retriever, "should_process_file", recording)
    return seen


def test_excluded_directory_contents_are_never_visited(project, monkeypatch):
    seen = _visited_paths(monkeypatch)
    found = retrieve_file_paths(
        [project], ["*.js", "*.json"], ["node_modules/**"], False, None
    )
    assert sorted(str(p) for p in found) == [
        str(project / "package.json"),
        str(project / "src" / "app.js"),
    ]
    visited_inside = [
        p for p in seen if "node_modules" in p.parts and p != project / "node_modules"
    ]
    assert visited_inside == []


def test_excluded_directory_itself_is_still_listed_but_not_descended(
    project, monkeypatch
):
    # The directory entry itself is yielded (and filtered out as "not a
    # file"), only its contents are skipped.
    seen = _visited_paths(monkeypatch)
    retrieve_file_paths([project], ["*.js"], ["node_modules/**"], False, None)
    assert project / "node_modules" in seen


def test_nested_excluded_directory_is_pruned(tmp_path, monkeypatch):
    (tmp_path / "a" / "node_modules").mkdir(parents=True)
    (tmp_path / "a" / "node_modules" / "x.js").write_text("x\n")
    (tmp_path / "a" / "keep.js").write_text("keep\n")
    seen = _visited_paths(monkeypatch)
    found = retrieve_file_paths([tmp_path], ["*.js"], ["node_modules/**"], False, None)
    assert [str(p) for p in found] == [str(tmp_path / "a" / "keep.js")]
    assert tmp_path / "a" / "node_modules" / "x.js" not in seen


def test_extension_exclude_does_not_prune_directories(tmp_path, monkeypatch):
    (tmp_path / "logs").mkdir()
    (tmp_path / "logs" / "a.log").write_text("log\n")
    (tmp_path / "logs" / "b.txt").write_text("txt\n")
    seen = _visited_paths(monkeypatch)
    found = retrieve_file_paths([tmp_path], [], ["*.log"], False, None)
    assert [str(p) for p in found] == [str(tmp_path / "logs" / "b.txt")]
    # *.log can only match files, so the directory must still be visited.
    assert tmp_path / "logs" / "a.log" in seen


def test_bare_directory_name_pattern_does_not_prune(tmp_path, monkeypatch):
    # `node_modules` without `/**` excludes no contents at file level
    # today (fnmatch needs a full match), so pruning must not kick in
    # either — pruning follows the existing matcher exactly.
    (tmp_path / "node_modules").mkdir()
    (tmp_path / "node_modules" / "x.js").write_text("x\n")
    seen = _visited_paths(monkeypatch)
    found = retrieve_file_paths([tmp_path], ["*.js"], ["node_modules"], False, None)
    assert [str(p) for p in found] == [str(tmp_path / "node_modules" / "x.js")]
    assert tmp_path / "node_modules" / "x.js" in seen


@pytest.mark.parametrize(
    "pattern, dir_name, expected",
    [
        ("node_modules/**", "node_modules", True),
        ("node_modules/**", "src", False),
        ("*.log", "logs", False),
        ("node_modules", "node_modules", False),
        ("build/**", "build", True),
        # The existing `**` matcher is substring-based: `src/**/generated/**`
        # already excludes every file under src/ at file level, so pruning
        # src/ preserves today's output exactly.
        ("src/**/generated/**", "src", True),
        ("src/**/generated/**", "other", False),
    ],
)
def test_is_excluded_directory(pattern, dir_name, expected):
    assert is_excluded_directory(Path(dir_name), [pattern], False) is expected


def test_traversal_order_matches_rglob(tmp_path):
    (tmp_path / "sub1" / "deep").mkdir(parents=True)
    (tmp_path / "sub1" / "b.txt").touch()
    (tmp_path / "sub1" / "deep" / "c.txt").touch()
    (tmp_path / "sub2").mkdir()
    (tmp_path / "sub2" / "d.txt").touch()
    (tmp_path / "a.txt").touch()
    assert [str(p) for p in _iter_tree(tmp_path, [], False)] == [
        str(p) for p in tmp_path.rglob("*")
    ]
