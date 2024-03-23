import os
import sys
import workspace_service

from simple_term_menu import TerminalMenu


def render_main_menu():
    options = ["[o] Open workspace", "[a] Add workspace", "[c] Change workspace", "[d] Delete workspace", "[q] Quit"]
    quit = False
    while not quit:
        os.system('clear')
        main_menu = TerminalMenu(options)
        main_menu_entry_index = main_menu.show()
        selected_option = options[main_menu_entry_index]
        if selected_option == "[q] Quit":
            quit = True
        elif selected_option == "[a] Add workspace":
            add_workspace(None, [])
        elif selected_option == "[c] Change workspace":
            handle_workspace(add_workspace)
        elif selected_option == "[o] Open workspace":
            handle_workspace(workspace_service.open_workspace)
        elif selected_option == "[d] Delete workspace":
            handle_workspace(workspace_service.delete_workspace)

    print("Exiting")
    sys.exit(0)

def handle_workspace(handler):
    workspaces = workspace_service.list_workspaces()
    change_menu = TerminalMenu(workspaces)
    change_indicies = change_menu.show()
    workspace = workspaces[change_indicies]
    workspace_apps = workspace_service.load_workspace(workspace)
    handler(workspace, workspace_apps)

def add_workspace(name: str | None, workspace_apps: list[str]):
    choosen_name = name if name is not None else choose_name()

    applications = workspace_service.available_applications()
    names = workspace_service.application_names(applications)
    workspace_apps_names = workspace_service.application_names(workspace_apps)
    # In case we have invalid apps (can be deleted or whatever reason) remove it from the preselection
    # If the workspace is saved the invalid app will be removed
    valid_names = list(set(names) & set(workspace_apps_names))

    application_list_terminal = TerminalMenu(names, multi_select=True, show_multi_select_hint=True, preselected_entries=valid_names, multi_select_select_on_accept=False)
    applications_indicies = application_list_terminal.show()
    selected_apps = [applications[index] for index in applications_indicies]
    confirmation = confirm_workspace_creation(selected_apps)
    if confirmation.lower() in ('y', 'yes'):
        workspace_service.save_workspace(choosen_name, selected_apps)

def choose_name():
    name = input("Workspace name: ")
    name_available = workspace_service.check_name_availability(name)
    if name_available:
        return name

    print(f"Workspace with name {name} is not available")
    try_again = input("Do you wish to choose another name? ")
    if not try_again.lower() in ('y', 'yes'):
        sys.exit(0)

    add_workspace(None, [])

def confirm_workspace_creation(selected_apps: list[str]):
    selected_names = workspace_service.application_names(selected_apps)
    print(*selected_names, sep="\n")
    return input("\nDo you wish to create specified workspace? [y/yes] ")


