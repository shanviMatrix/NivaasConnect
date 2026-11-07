from getpass import getpass

import psycopg
from psycopg.errors import UniqueViolation

from app.core.config import settings
from app.core.security import hash_password


def main():
    username = input("Enter Admin username: ").strip()

    if len(username) < 3 or len(username) > 80:
        print("Username must contain between 3 and 80 characters.")
        return

    password = getpass("Enter Admin password (minimum 12 characters): ")
    confirm_password = getpass("Confirm Admin password: ")

    if len(password) < 12:
        print("Password must be at least 12 characters long.")
        return

    if password != confirm_password:
        print("Passwords do not match.")
        return

    hashed_password = hash_password(password)

    try:
        with psycopg.connect(settings.database_conninfo) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO user_accounts (
                        username,
                        password_hash,
                        role
                    )
                    VALUES (%s, %s, 'Admin')
                    RETURNING account_id
                    """,
                    (username, hashed_password),
                )
                account_id = cursor.fetchone()[0]

        print(f"Admin account created successfully. Account ID: {account_id}")

    except UniqueViolation:
        print("This username already exists.")


if __name__ == "__main__":
    main()
