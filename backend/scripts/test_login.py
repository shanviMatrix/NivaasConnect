from getpass import getpass

import httpx


BASE_URL = "http://127.0.0.1:8000/api/v1"


def main():
    username = input("Admin username: ").strip()
    password = getpass("Admin password: ")

    try:
        with httpx.Client(timeout=10) as client:
            response = client.post(
                f"{BASE_URL}/auth/login",
                json={
                    "username": username,
                    "password": password,
                },
            )

            if response.status_code != 200:
                print("LOGIN FAILED:", response.status_code, response.text)
                return

            data = response.json()
            token = data["access_token"]

            print("\nLOGIN SUCCESSFUL")
            print("Token received:", bool(token))
            print("Token type:", data["token_type"])
            print("User:", data["user"])

            profile_response = client.get(
                f"{BASE_URL}/auth/me",
                headers={"Authorization": f"Bearer {token}"},
            )

            print("\nTOKEN VERIFICATION STATUS:", profile_response.status_code)

            if profile_response.status_code == 200:
                print("Verified profile:", profile_response.json())
                print("\nAUTHENTICATION FLOW: SUCCESS")
            else:
                print("Profile verification failed:", profile_response.text)

    except httpx.ConnectError:
        print("Could not connect. Is the FastAPI server running?")


if __name__ == "__main__":
    main()
