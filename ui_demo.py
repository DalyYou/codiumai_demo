import time

from playwright.sync_api import Playwright, sync_playwright, expect


class PlayClient:
    def __init__(self, base_url='http://localhost:9009/docs'):
        self.base_url = base_url
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=False, channel="chrome", args=["--start-maximized"])
        self.context = self.browser.new_context()
        self.page = self.context.new_page()

    def close(self):
        self.context.close()
        self.browser.close()

    def goto_page(self, url=None):
        self.page.goto(self.base_url) if url is None else self.page.goto(url)

    def fill_by_label(self, selector, value):
        self.page.get_by_label(selector).fill(value)


class LoginPage:

    def __init__(self):
        self.play_client = PlayClient()

    def login(self, user, password):
        """
        Logs in the user with the given credentials.

        Args:
            user (str): The username of the user.
            password (str): The password of the user.

        Returns:
            bool: True if the login was successful, False otherwise.
        """
        try:
            self.play_client.goto_page()
            self.play_client.page.get_by_role("button", name="Authorize").click()
            self.play_client.fill_by_label("username:", user)
            self.play_client.fill_by_label("password:", password)
            self.play_client.page.get_by_label("Apply given OAuth2 credentials").click()
            time.sleep(5)
            self.play_client.page.get_by_role("button", name="Close").click()
            return True
        except Exception as e:
            raise Exception("Login failed: " + str(e))


login_page = LoginPage()
login_page.login('user1', 'secret1')
