from sysinfo import create_project_directory, project_path
from gui import create_frame, gui_config, content, keyword_submit_clicked


# PATH CREATION IF NON-EXISTENT
create_project_directory(project_path)

# GUI
root = create_frame()
gui_config(root)
content(root)

# Callback functions
keyword_submit_clicked()
root.mainloop()

