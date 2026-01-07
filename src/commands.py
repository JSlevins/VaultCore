from getpass import getpass
import re

from src.models import User, UserRole
from src.security import hash_password

def create_admin(db_session):
    admin_exists = db_session.query(User).filter_by(is_admin=True).first()
    if admin_exists:
        print("Admin already exists. Aborting...")
        return

    # Inputs
    username = input("Username: ").strip()
    password = getpass("Password: ")
    password2 = getpass("Confirm Password: ")
    email = input("Email address: ").strip()

    # Inputs validation
    if user_creation_validation(username, password, password2, email):
        admin = User(
            username=username,
            password_hash=hash_password(password),
            email=email,
            role=UserRole.ADMIN
        )

        db_session.add(admin)
        db_session.commit()
        print("Admin user was successfully created")

def create_editor(db_session):
    # Inputs
    username = input("Username: ").strip()
    password = getpass("Password: ")
    password2 = getpass("Confirm Password: ")
    email = input("Email address: ").strip()

    # Inputs validation
    if user_creation_validation(username, password, password2, email):
        editor = User(
            username=username,
            password_hash=hash_password(password),
            email=email,
            role=UserRole.EDITOR
        )

        db_session.add(editor)
        db_session.commit()
        print("Editor user was successfully created")


def user_creation_validation(username: str, password: str, password2:str, email: str) -> bool:
    error_msg = []
    if not username:
        error_msg.append("Username required.")

    if password != password2:
        error_msg.append("Passwords don't match.")

    if len(password) < 8:
        error_msg.append("Password must be at least 8 characters long.")

    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not re.match(pattern, email):
        error_msg.append("Invalid email.")

    if error_msg:
        print(f"\nAdmin wasn't created:")
        for i, msg in enumerate(error_msg, 1):
            print(f"{i}. {msg}")
        print("\n")
        return False
    return True