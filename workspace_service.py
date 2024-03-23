import sys
import os
from pathlib import Path

APPLICATIONS_BASE = "/Applications/"
SAVED_BASE = "./saved"

def command_line_runner(workspace: str):
    workspaces = list_workspaces()
    if not workspace in workspaces:
        print(f"Workspace {workspace} do not exist")
        sys.exit(0)

    workspace_apps = load_workspace(workspace)
    open_workspace(workspace, workspace_apps)

def list_workspaces():
    workspaces = Path(f"{SAVED_BASE}/") 
    return [workspace.name for workspace in workspaces.iterdir()]

def open_workspace(name: str, applications: list[str]):
    OPEN_COMMAND = "open"

    print(f"Opening workspace {name}")
    for app in applications:
        app_path = Path(f"{APPLICATIONS_BASE}/{app}")
        if not app_path.exists():
            print(f"Application {app} do not exists. Skipping") 
            continue
        command = f"{OPEN_COMMAND} {APPLICATIONS_BASE}/{app}"
        os.system(command)

def save_workspace(name: str, selected_apps: list[str]):
    workspace_to_save = Path(f"{SAVED_BASE}/{name}")
    formated_save = '\n'.join(map(str, selected_apps))
    workspace_to_save.write_text(formated_save)
    print(f"Workspace {name} sucessfully saved")

def delete_workspace(name: str, applications: list[str]):
    app_names = application_names(applications)
    print(name)
    print(*app_names, sep="\n")
    confirmed = input("Do you wish to delete above workspace? [y/yes] ")
    if confirmed.lower() in ('y', 'yes'):
        Path(f"{SAVED_BASE}/{name}").unlink()

def load_workspace(workspace_name: str):
    file_path = f"{SAVED_BASE}/{workspace_name}"
    entries = []
    with open(file_path, 'r') as file:
        for line in file:
            # Remove leading/trailing whitespace and newline characters
            entries.append(line.strip())  
    return entries

def check_name_availability(name: str):
    saved = Path(SAVED_BASE)
    if not saved.exists():
        saved.mkdir(parents=True)
        return True
     
    available = True
    for workspace in saved.iterdir():
        if workspace.name == name:
            available = False
            break

    return available
    

def available_applications():
    """
        List all applications in '/Appications' folder.
    """
    folder = Path(APPLICATIONS_BASE)
    if folder.is_dir():
        available_applications = [item.name for item in folder.iterdir() if item.name is not None and item.name.endswith(".app")]
        return available_applications
    else:
        print(f"Folder {APPLICATIONS_BASE} not existing or not a folder")
        sys.exit(1)
            
def application_names(apps: list[str]):
    """
        Extract the names from the list of applications -> so from strign 'application.app' will be 'application'
    """
    names = [app.split(".")[0] for app in apps.__iter__()]
    return names

