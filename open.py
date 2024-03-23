import os
import sys
from simple_term_menu import TerminalMenu
from pathlib import Path


# This may be changed based on OS
APPLICATIONS_BASE = "/Applications/"
SAVED_BASE = "./saved"

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

def render_main_menu():
    os.system('clear')
    options = ["[o] Open workspace", "[a] Add workspace", "[c] Change workspace", "[d] Delete workspace", "[q] Quit"]
    main_menu = TerminalMenu(options)
    main_menu_entry_index = main_menu.show()
    selected_option = options[main_menu_entry_index]
    if selected_option == "[q] Quit":
        print("Exiting")
        sys.exit(0)
    elif selected_option == "[a] Add workspace":
        add_workspace(None, [])
    elif selected_option == "[c] Change workspace":
        handle_workspace(add_workspace)
    elif selected_option == "[o] Open workspace":
        handle_workspace(open_workspace)
    elif selected_option == "[d] Delete workspace":
        handle_workspace(delete_workspace)

def handle_workspace(handler):
    workspaces = list_workspaces()
    change_menu = TerminalMenu(workspaces)
    change_indicies = change_menu.show()
    workspace = workspaces[change_indicies]
    workspace_apps = load_workspace(workspace)
    handler(workspace, workspace_apps)

def delete_workspace(name: str, applications: list[str]):
    app_names = application_names(applications)
    print(name)
    print(*app_names, sep="\n")
    confirmed = input("Do you wish to delete above workspace? [y/yes] ")
    if confirmed.lower() in ('y', 'yes'):
        Path(f"{SAVED_BASE}/{name}").unlink()
    render_main_menu()

def list_workspaces():
    workspaces = Path(f"{SAVED_BASE}/") 
    return [workspace.name for workspace in workspaces.iterdir()]

def load_workspace(workspace_name: str):
    file_path = f"{SAVED_BASE}/{workspace_name}"
    entries = []
    with open(file_path, 'r') as file:
        for line in file:
            # Remove leading/trailing whitespace and newline characters
            entries.append(line.strip())  
    return entries

def add_workspace(name: str | None, workspace_apps: list[str]):
    choosen_name = name if name is not None else choose_name()

    applications = available_applications()
    names = application_names(applications)
    workspace_apps_names = application_names(workspace_apps)
    # In case we have invalid apps (can be deleted or whatever reason) remove it from the preselection
    # If the workspace is saved the invalid app will be removed
    valid_names = list(set(names) & set(workspace_apps_names))

    application_list_terminal = TerminalMenu(names, multi_select=True, show_multi_select_hint=True, preselected_entries=valid_names, multi_select_select_on_accept=False)
    applications_indicies = application_list_terminal.show()
    selected_apps = [applications[index] for index in applications_indicies]
    confirmation = confirm_workspace_creation(selected_apps)
    if confirmation == 'y':
        save_workspace(choosen_name, selected_apps)

    render_main_menu()

def choose_name():
    name = input("Workspace name: ")
    name_available = check_name_availability(name)
    if name_available:
        return name

    print(f"Workspace with name {name} is not available")
    try_again = input("Do you wish to choose another name? ")
    if not try_again.lower() in ('y', 'yes'):
        sys.exit(0)

    add_workspace(None, [])

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
    
def confirm_workspace_creation(selected_apps: list[str]):
    selected_names = application_names(selected_apps)
    print(*selected_names, sep="\n")
    return input("\nDo you wish to create specified workspace? ")

def save_workspace(name: str, selected_apps: list[str]):
    workspace_to_save = Path(f"{SAVED_BASE}/{name}")
    formated_save = '\n'.join(map(str, selected_apps))
    workspace_to_save.write_text(formated_save)
    print(f"Workspace {name} sucessfully saved")

def command_line_runner(workspace: str):
    workspaces = list_workspaces()
    if not workspace in workspaces:
        print(f"Workspace {workspace} do not exist")
        sys.exit(0)

    workspace_apps = load_workspace(workspace)
    open_workspace(workspace, workspace_apps)




def main():
    if len(sys.argv) > 1:
        workspace = sys.argv[1]
        command_line_runner(workspace)
    else:
        render_main_menu()


if __name__ == "__main__":
    main()


