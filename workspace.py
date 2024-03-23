import sys
import menu
import workspace_service

def main():
    if len(sys.argv) > 1:
        workspace = sys.argv[1]
        workspace_service.command_line_runner(workspace)
    else:
        menu.render_main_menu()


if __name__ == "__main__":
    main()


