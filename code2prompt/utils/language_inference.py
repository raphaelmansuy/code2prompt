import os


def infer_language(filename: str, syntax_map: dict) -> str:
    """
    Infers the programming language of a given file based on its extension.

    Parameters:
    - filename (str): The name of the file including its extension.
    - syntax_map (dict): Custom syntax mappings for language inference.

    Returns:
    - str: The inferred programming language as a lowercase string, e.g., "python".
           Returns "unknown" if the language cannot be determined.
    """
    _, extension = os.path.splitext(filename)
    extension = extension.lower()

    # Check user-defined syntax map first
    if extension in syntax_map:
        return syntax_map[extension]

    language_map = {
        ".c": "c",
        ".h": "c",
        ".cpp": "cpp",
        ".hpp": "cpp",
        ".cc": "cpp",
        ".cxx": "cpp",
        ".java": "java",
        ".js": "javascript",
        ".jsx": "javascript",
        ".ts": "typescript",
        ".tsx": "typescript",
        ".cs": "csharp",
        ".php": "php",
        ".go": "go",
        ".rs": "rust",
        ".kt": "kotlin",
        ".swift": "swift",
        ".scala": "scala",
        ".dart": "dart",
        ".py": "python",
        ".rb": "ruby",
        ".pl": "perl",
        ".pm": "perl",
        ".sh": "bash",
        ".bash": "bash",
        ".zsh": "zsh",
        ".ps1": "powershell",
        ".html": "html",
        ".htm": "html",
        ".xml": "xml",
        ".sql": "sql",
        ".m": "matlab",
        ".r": "r",
        ".lua": "lua",
        ".jl": "julia",
        ".f": "fortran",
        ".f90": "fortran",
        ".hs": "haskell",
        ".lhs": "haskell",
        ".ml": "ocaml",
        ".erl": "erlang",
        ".ex": "elixir",
        ".exs": "elixir",
        ".clj": "clojure",
        ".coffee": "coffeescript",
        ".groovy": "groovy",
        ".pas": "pascal",
        ".vb": "visualbasic",
        ".asm": "assembly",
        ".s": "assembly",
        ".lisp": "lisp",
        ".cl": "lisp",
        ".scm": "scheme",
        ".rkt": "racket",
        ".fs": "fsharp",
        ".d": "d",
        ".ada": "ada",
        ".nim": "nim",
        ".cr": "crystal",
        ".v": "verilog",
        ".vhd": "vhdl",
        ".tcl": "tcl",
        ".elm": "elm",
        ".zig": "zig",
        ".raku": "raku",
        ".perl6": "raku",
        ".p6": "raku",
        ".vim": "vimscript",
        ".ps": "postscript",
        ".prolog": "prolog",
        ".cobol": "cobol",
        ".cob": "cobol",
        ".cbl": "cobol",
        ".forth": "forth",
        ".fth": "forth",
        ".abap": "abap",
        ".apex": "apex",
        ".sol": "solidity",
        ".hack": "hack",
        ".sml": "standardml",
        ".purs": "purescript",
        ".idr": "idris",
        ".agda": "agda",
        ".lean": "lean",
        ".wasm": "webassembly",
        ".wat": "webassembly",
        ".j2": "jinja2",
        ".md": "markdown",
        ".tex": "latex",
        ".bib": "bibtex",
        ".yaml": "yaml",
        ".yml": "yaml",
        ".json": "json",
        ".toml": "toml",
        ".ini": "ini",
        ".cfg": "ini",
        ".conf": "ini",
        ".dockerfile": "dockerfile",
        ".docker": "dockerfile",
        '.txt': 'plaintext',
        '.csv': 'csv',
        '.tsv': 'tsv',
        '.log': 'log'
    }

    return language_map.get(extension, "unknown")
