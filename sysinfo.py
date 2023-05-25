from os import getlogin, environ, path, mkdir


def create_project_directory(project_directory):
    """
        Creates the project path if it does not exist.
    """
    if not path.exists(project_directory):
        mkdir(project_directory)


try:
    username = getlogin() or environ.get('USERNAME') or environ.get('USER') or ""  # Get username from OS
    system_root = environ.get('SYSTEMROOT')  # Find Windows directory
    root_drive = system_root.split("\\")[0]  # Fetch the root drive by splitting at index 0
    project_path = f'{root_drive}\\Users\\{username}\\Desktop\\Wikipedia Web Scraping And Document Comparison'
    create_project_directory(project_path)  # Call the create_project_directory function with the project_path

except OSError as oe:
    print(f"Error: {oe}")
except Exception as e:
    print(f"Error: {e}")
