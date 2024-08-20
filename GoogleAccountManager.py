import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from AntiDetect import AntiDetect


class GoogleAccountManager:
    def __init__(self, email, old_password, new_password, first_name, last_name, dob, backup_email, proxy=None,
                 user_agent=None):
        self.email = email
        self.old_password = old_password
        self.new_password = new_password
        self.first_name = first_name
        self.last_name = last_name
        self.dob = dob
        self.backup_email = backup_email
        self.antidetect = AntiDetect(proxy=proxy, user_agent=user_agent)
        self.driver = self.antidetect.apply_settings()

    def login(self):
        """Вход в аккаунт гугла"""
        try:
            self.driver.get("https://accounts.google.com/signin/v2/identifier")
            self.driver.find_element(By.ID, "identifierId").send_keys(self.email + Keys.RETURN)
            time.sleep(2)
            self.driver.find_element(By.NAME, "password").send_keys(self.old_password + Keys.RETURN)
            time.sleep(2)
        except Exception as e:
            print(f"Login failed: {e}")

    def change_name(self):
        """Изменение имени"""
        try:
            self.driver.get("https://myaccount.google.com/personal-info")
            time.sleep(2)
            self.driver.find_element(By.XPATH, "//span[text()='Имя']").click()
            time.sleep(2)
            first_name_input = self.driver.find_element(By.XPATH, "//input[@name='firstName']")
            last_name_input = self.driver.find_element(By.XPATH, "//input[@name='lastName']")
            first_name_input.clear()
            first_name_input.send_keys(self.first_name)
            last_name_input.clear()
            last_name_input.send_keys(self.last_name)
            self.driver.find_element(By.XPATH, "//button/span[text()='Сохранить']").click()
        except Exception as e:
            print(f"Failed to change name: {e}")
        return self.first_name, self.last_name

    def change_password(self):
        """Изменение пароля"""
        try:
            self.driver.get("https://myaccount.google.com/security-checkup/password")
            time.sleep(2)
            self.driver.find_element(By.NAME, "password").send_keys(self.old_password)
            self.driver.find_element(By.NAME, "newPassword").send_keys(self.new_password)
            self.driver.find_element(By.NAME, "confirmPassword").send_keys(self.new_password)
            self.driver.find_element(By.XPATH, "//button/span[text()='Сохранить']").click()
        except Exception as e:
            print(f"Failed to change password: {e}")

    def save_to_csv(self):
        """Сохранение в таблицу"""
        try:
            data = {
                "email": self.email,
                "new_password": self.new_password,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "dob": self.dob,
                "backup_email": self.backup_email
            }
            df = pd.DataFrame([data])
            df.to_csv('google_accounts.csv', mode='a', header=False, index=False)
        except Exception as e:
            print(f"Failed to save data to CSV: {e}")

    def run(self):
        try:
            self.login()
            self.change_name()
            self.change_password()
            self.save_to_csv()
        finally:
            self.driver.quit()
