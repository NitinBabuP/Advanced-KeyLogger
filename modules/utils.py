import os

def get_user_log_folder(username: str) -> str:
    """Returns the path to the user's log folder."""
    base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
    user_folder = os.path.join(base_dir, username)
    os.makedirs(user_folder, exist_ok=True)
    return user_folder

def read_file_content(filepath: str) -> str:
    """Reads the content of a file safely."""
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return "No data available yet."
    except Exception as e:
        return f"Error reading file: {e}"
