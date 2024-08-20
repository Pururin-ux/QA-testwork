from GoogleAccountManager import GoogleAccountManager
from TwitterAccountManager import TwitterAccountManager
import random
import os


def load_proxies(file_path):
    """Загрузка прокси из файла"""
    try:
        with open(file_path, 'r') as file:
            proxies = [line.strip() for line in file]
        return proxies
    except FileNotFoundError:
        print(f"Proxy file not found: {file_path}")
        return []
    except Exception as e:
        print(f"Error loading proxies: {e}")
        return []


def load_user_agents(file_path):
    """Загрузка юзер-агентов из файла"""
    try:
        with open(file_path, 'r') as file:
            user_agents = [line.strip() for line in file]
        return user_agents
    except FileNotFoundError:
        print(f"User agents file not found: {file_path}")
        return []
    except Exception as e:
        print(f"Error loading user agents: {e}")
        return []


def main():
    # Загрузка прокси и юзер-агентов
    proxies = load_proxies("path")
    user_agents = load_user_agents("path")

    if not proxies:
        print("No proxies loaded. Exiting.")
        return

    if not user_agents:
        print("No user agents loaded. Exiting.")
        return

    # Ваш OpenAI API ключ
    openai_api_key = os.getenv('OPENAI_API_KEY', 'your_openai_api_key_here')

    # Создание и запуск GoogleAccountManager
    google_manager = GoogleAccountManager(
        email="your_google_email@gmail.com",
        old_password="old_password",
        new_password="new_secure_password",
        first_name="NewFirstName",
        last_name="NewLastName",
        dob="01/01/2000",
        backup_email="backup@example.com",
        proxy=random.choice(proxies),
        user_agent=random.choice(user_agents)
    )

    try:
        google_manager.run()
        print("Google account management completed successfully.")
    except Exception as e:
        print(f"Google account management failed: {e}")

    # Создание и запуск TwitterAccountManager
    twitter_manager = TwitterAccountManager(
        email="your_twitter_email",
        password="your_twitter_password",
        new_password="new_secure_password",
        openai_api_key=openai_api_key,
        proxy=random.choice(proxies),
        user_agent=random.choice(user_agents)
    )

    try:
        twitter_manager.run()
        print("Twitter account management completed successfully.")
    except Exception as e:
        print(f"Twitter account management failed: {e}")


if __name__ == "__main__":
    main()
