from code2prompt.comment_stripper import strip_comments
from code2prompt.utils.add_line_numbers import add_line_numbers
from code2prompt.utils.language_inference import infer_language
from datetime import datetime

def process_file(file_path, suppress_comments, line_number, no_codeblock):
    """
    Processes a given file to extract its metadata and content.

    Parameters:
    - file_path (Path): The path to the file to be processed.
    - suppress_comments (bool): Flag indicating whether to remove comments from the file content.
    - line_number (bool): Flag indicating whether to add line numbers to the file content.
    - no_codeblock (bool): Flag indicating whether to disable wrapping code inside markdown code blocks.

    Returns:
    dict: A dictionary containing the file information and content.
    """
    file_extension = file_path.suffix
    file_size = file_path.stat().st_size
    file_creation_time = datetime.fromtimestamp(file_path.stat().st_ctime).strftime("%Y-%m-%d %H:%M:%S")
    file_modification_time = datetime.fromtimestamp(file_path.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
    language = "unknown"

    try:
        with file_path.open("r", encoding="utf-8") as f:
            file_content = f.read()
        
        language = infer_language(file_path.name)
        
        if suppress_comments and language != "unknown":
            file_content = strip_comments(file_content, language)
        
        if line_number:
            file_content = add_line_numbers(file_content)
    except UnicodeDecodeError:
        return None

    return {
        "path": str(file_path),
        "extension": file_extension,
        "language": language,
        "size": file_size,
        "created": file_creation_time,
        "modified": file_modification_time,
        "content": file_content,
        "no_codeblock": no_codeblock
    }
