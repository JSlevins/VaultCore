import sys
from src.commands import create_admin, create_editor
from src.database import Session


def main():
    if len(sys.argv) < 2:
        print("Usage: python cli.py <command> [<args>]")
        print("Available commands: 'create-admin', 'create-editor'")
        return

    command = sys.argv[1]

    if command == "create-admin":
        db = Session()
        try:
            create_admin(db)
        finally:
            db.close()

    elif command == "create-editor":
        db = Session()
        try:
            create_editor(db)
        finally:
            db.close()

    else:
        print(f"{command} is not a valid command.")

if __name__ == "__main__":
    main()