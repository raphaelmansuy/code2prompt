

from code2prompt.generate_markdown_content import generate_markdown_content


def test_generate_markdown_content():
    files_data = [
        ("File 1 content", "/path/to/file1.py"),
        ("File 2 content", "/path/to/file2.py"),
        ("File 3 content", "/path/to/file3.py"),
    ]
    no_codeblock = False

    expected_output = (
        "# Table of Contents\n"
        "- /path/to/file1.py\n"
        "- /path/to/file2.py\n"
        "- /path/to/file3.py\n"
        "\n"
        "File 1 content"
        "File 2 content"
        "File 3 content"
    )

    assert generate_markdown_content(files_data, no_codeblock) == expected_output


def test_generate_markdown_content_with_no_codeblock():
    files_data = [
        ("File 1 content", "/path/to/file1.py"),
        ("File 2 content", "/path/to/file2.py"),
        ("File 3 content", "/path/to/file3.py"),
    ]
    no_codeblock = True

    expected_output = (
        "# Table of Contents\n"
        "- /path/to/file1.py\n"
        "- /path/to/file2.py\n"
        "- /path/to/file3.py\n"
        "\n"
        "File 1 content"
        "File 2 content"
        "File 3 content"
    )

    assert generate_markdown_content(files_data, no_codeblock) == expected_output