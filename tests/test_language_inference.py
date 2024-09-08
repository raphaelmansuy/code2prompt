import pytest
from code2prompt.utils.language_inference import infer_language

def test_infer_language():
    """ Test the infer_language function."""
    syntax_map = {}  # Define the syntax map as needed
    assert infer_language("main.c", syntax_map) == "c"  # Added syntax_map argument
    assert infer_language("main.cpp", syntax_map) == "cpp"
    assert infer_language("Main.java", syntax_map) == "java"
    assert infer_language("script.js", syntax_map) == "javascript"
    assert infer_language("Program.cs", syntax_map) == "csharp"
    assert infer_language("index.php", syntax_map) == "php"
    assert infer_language("main.go", syntax_map) == "go"
    assert infer_language("lib.rs", syntax_map) == "rust"
    assert infer_language("app.kt", syntax_map) == "kotlin"
    assert infer_language("main.swift", syntax_map) == "swift"
    assert infer_language("Main.scala", syntax_map) == "scala"
    assert infer_language("main.dart", syntax_map) == "dart"
    assert infer_language("script.py", syntax_map) == "python"
    assert infer_language("script.rb", syntax_map) == "ruby"
    assert infer_language("script.pl", syntax_map) == "perl"
    assert infer_language("script.sh", syntax_map) == "bash"
    assert infer_language("script.ps1", syntax_map) == "powershell"
    assert infer_language("index.html", syntax_map) == "html"
    assert infer_language("data.xml", syntax_map) == "xml"
    assert infer_language("query.sql", syntax_map) == "sql"
    assert infer_language("script.m", syntax_map) == "matlab"
    assert infer_language("script.r", syntax_map) == "r"
    assert infer_language("file.txt", syntax_map) == "plaintext"
