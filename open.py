import os
import sys
from pathlib import Path

# TODO: Load from file
apps = [r"/Applications/Microsoft\ Teams\ \(work\ or\ school\).app", "/Applications/WhatsApp.app"]


# TODO: Create saving to file
# TODO: Create menu
#           - Create session command or Update session (load from file)
#           - Load apps from /Applications/ (not sure if brew add there as well -> check)
#           - Display apps -> How can I do navigation like in fish? or htop
#           - With 'x' the app will be appended to file -> Probably load 
def open(applications: list[str]):
    OPEN_COMMAND = "open"

    for app in applications:
        command = f"{OPEN_COMMAND} {app}"
        os.system(command)

def render_menu():
    APPLICATIONS_BASE = "/Applications/"
    folder = Path(APPLICATIONS_BASE)
    if folder.is_dir():
        available_applications = [item.name for item in folder.iterdir()]
        return available_applications
    else:
        print(f"Folder {APPLICATIONS_BASE} not existing or not a folder")
        sys.exit(1)
            
#open(apps)
print(render_menu())
