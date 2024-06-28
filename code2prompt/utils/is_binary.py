def is_binary(file_path):
    try:
        with open(file_path, "rb") as file:
            chunk = file.read(1024)
            return b"\x00" in chunk
    except IOError:
        print(f"Error: The file at {file_path} could not be opened.")
        return False