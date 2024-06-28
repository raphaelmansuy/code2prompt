from code2prompt.utils.generate_markdown_content import generate_markdown_content

def test_generate_markdown_content():
    # Define sample files data
    files_data = [
        {
            'path': 'file1.py',
            'extension': 'py',
            'language': 'python',
            'size': 100,
            'created': '2022-01-01',
            'modified': '2022-01-02',
            'content': 'print("Hello, World!")',
        },
        {
            'path': 'file2.txt',
            'extension': 'txt',
            'language': 'unknown',
            'size': 50,
            'created': '2022-01-03',
            'modified': '2022-01-04',
            'content': 'Sample text content',
        },
    ]

    # Test with no_codeblock=False
    expected_output = (
        "# Table of Contents\n"
        "- file1.py\n"
        "- file2.txt\n\n"
        "## File: file1.py\n\n"
        "- Extension: py\n"
        "- Language: python\n"
        "- Size: 100 bytes\n"
        "- Created: 2022-01-01\n"
        "- Modified: 2022-01-02\n\n"
        "### Code\n\n```python\nprint(\"Hello, World!\")\n```\n\n"
        "## File: file2.txt\n\n"
        "- Extension: txt\n"
        "- Language: unknown\n"
        "- Size: 50 bytes\n"
        "- Created: 2022-01-03\n"
        "- Modified: 2022-01-04\n\n"
        "### Code\n\n```unknown\nSample text content\n```\n\n"
    )
    assert generate_markdown_content(files_data, no_codeblock=False) == expected_output

    # Test with no_codeblock=True
    expected_output_no_codeblock = (
        "# Table of Contents\n"
        "- file1.py\n"
        "- file2.txt\n\n"
        "## File: file1.py\n\n"
        "- Extension: py\n"
        "- Language: python\n"
        "- Size: 100 bytes\n"
        "- Created: 2022-01-01\n"
        "- Modified: 2022-01-02\n\n"
        "### Code\n\nprint(\"Hello, World!\")\n\n"
        "## File: file2.txt\n\n"
        "- Extension: txt\n"
        "- Language: unknown\n"
        "- Size: 50 bytes\n"
        "- Created: 2022-01-03\n"
        "- Modified: 2022-01-04\n\n"
        "### Code\n\nSample text content\n\n"
    )
    assert generate_markdown_content(files_data, no_codeblock=True) == expected_output_no_codeblock