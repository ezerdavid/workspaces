import os



os.system("shopt -s extglob")
os.system(r"open /Applications/Microsoft\ Teams\ \(work\ or\ school\).app")
os.system("open /Applications/WhatsApp.app")


apps = [r"/Applications/Microsoft\ Teams\ \(work\ or\ school\).app", "/Applications/WhatsApp.app"]

def open(applications: list[str]):
    OPEN_COMMAND = "open"
    for app in applications:
        command = f"{OPEN_COMMAND} {app}"
        os.system(command)

