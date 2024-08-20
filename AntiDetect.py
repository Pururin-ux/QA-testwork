from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


class AntiDetect:
    def __init__(self, proxy=None, user_agent=None):
        self.proxy = proxy
        self.user_agent = user_agent

    def apply_settings(self):
        chrome_options = Options()

        # Скрытие автоматизации
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")

        # Настройки прокси и пользовательского агента
        if self.proxy:
            chrome_options.add_argument(f"--proxy-server={self.proxy}")
        if self.user_agent:
            chrome_options.add_argument(f"user-agent={self.user_agent}")

        # Настройка размера окна
        chrome_options.add_argument("window-size=1920,1080")

        # Добавление расширений (если необходимо)
        # chrome_options.add_extension('path/to/extension.crx')

        # Дополнительные настройки для фингерпринтинга
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-software-rasterizer")

        # Запуск драйвера
        service = Service(executable_path="path/to/chromedriver")
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver
