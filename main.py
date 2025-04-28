import os
import random
import string
import requests


def generate_random_id(length=14):
    safe_characters = string.ascii_letters + string.digits + "#*!§$%&/()=?.,<>-_+`"
    return ''.join(random.choice(safe_characters) for _ in range(length))


def check_network():
    try:
        response = requests.get('https://google.com', timeout=5)
        if response.status_code == 200:
            return True
        else:
            print("Network check failed. Retrying...")
            return False
    except requests.RequestException:
        print("No network or unable to connect.")
        return False


def get_or_generate_id():
    if os.path.exists("id"):
        with open("id", "r") as f:
            return f.read().strip()

    print("ID does not exist. Creating a new one...")
    new_id = generate_random_id()
    with open("id", "w") as f:
        f.write(new_id)

    return new_id


def main():
    print("starting")
    print("           ___     ____  _____")
    print("|   |     /  \\    |  |  |")
    print("|___|    /    \\   |--|  | ____")
    print("|   |   /------\\  |  \\  |    |")
    print("|   |  /        \\ |   \\ |____|")
    print("________________________________")
    print("HARG.14 by Timo Streich")
    print("\nstart running")

    check_network()

    # ID abrufen oder generieren
    id = get_or_generate_id()

    # Deine ID ausgeben
    print(f"Your public ID is: {id}")


if __name__ == "__main__":
    main()
