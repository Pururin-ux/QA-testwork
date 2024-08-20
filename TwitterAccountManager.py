import time
import openai
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from AntiDetect import AntiDetect


class TwitterAccountManager:
    def __init__(self, email, password, new_password, openai_api_key, proxy=None, user_agent=None):
        self.email = email
        self.password = password
        self.new_password = new_password
        self.openai_api_key = openai_api_key
        self.antidetect = AntiDetect(proxy=proxy, user_agent=user_agent)
        self.driver = self.antidetect.apply_settings()

    def login(self):
        """Вход в аккаунт твиттера"""
        try:
            self.driver.get("https://twitter.com/login")
            time.sleep(2)
            self.driver.find_element(By.NAME, "session[username_or_email]").send_keys(self.email)
            self.driver.find_element(By.NAME, "session[password]").send_keys(self.password + Keys.RETURN)
            time.sleep(2)
        except Exception as e:
            print(f"Login failed: {e}")

    def change_password(self):
        """Изменение пароля """
        try:
            self.driver.get("https://twitter.com/settings/password")
            time.sleep(2)
            self.driver.find_element(By.NAME, "current_password").send_keys(self.password)
            self.driver.find_element(By.NAME, "new_password").send_keys(self.new_password)
            self.driver.find_element(By.NAME, "password_confirmation").send_keys(self.new_password)
            self.driver.find_element(By.XPATH, "//div[text()='Save']").click()
        except Exception as e:
            print(f"Password change failed: {e}")

    @staticmethod
    def generate_tweet(api_key):
        """
        Генерация рандомного твита с ChatGPT
        """
        openai.api_key = api_key
        try:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt="Generate a random tweet on any topic.",
                max_tokens=50
            )
            return response.choices[0].text.strip()
        except Exception as e:
            print(f"Tweet generation failed: {e}")
            return "Here's a default tweet as fallback."

    def post_tweet(self):
        """Постинг твита"""
        try:
            tweet = self.generate_tweet(self.openai_api_key)
            self.driver.get("https://twitter.com/compose/tweet")
            time.sleep(2)
            tweet_box = self.driver.find_element(By.XPATH, "//div[@aria-label='Tweet text']")
            tweet_box.send_keys(tweet)
            self.driver.find_element(By.XPATH, "//div[@data-testid='tweetButtonInline']").click()
        except Exception as e:
            print(f"Posting tweet failed: {e}")

    def run(self):
        try:
            self.login()
            self.change_password()
            self.post_tweet()
        finally:
            self.driver.quit()
