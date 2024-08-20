from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


class AntiDetect:
    def __init__(self, proxy=None, user_agent=None):
        self.proxy = proxy
        self.user_agent = user_agent

    def apply_settings(self):

        chrome_options = Options()

        chrome_options.add_argument("--disable-blink-features=AutomationControlled")

        if self.proxy:
            chrome_options.add_argument(f"--proxy-server={self.proxy}")

        if self.user_agent:
            chrome_options.add_argument(f"user-agent={self.user_agent}")

        service = Service(executable_path="path/to/chromedriver")

        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver
