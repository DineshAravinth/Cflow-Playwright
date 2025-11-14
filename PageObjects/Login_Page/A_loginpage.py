from playwright.sync_api import Page
from Utilities.BaseHelpers import BaseHelper

class LoginPage:
    def __init__(self, page: Page, timeout: int = 30):
        self.page = page
        self.timeout = timeout
        self.helper = BaseHelper(page)

        # ✅ Locators (use XPATH for BaseHelper)
        self.textbox_clientid_xpath = '//*[@id="client-id"]'
        self.textbox_username_xpath = '//*[@id="username"]'
        self.textbox_password_xpath = '//*[@id="password"]'
        self.button_login_xpath = "//button[contains(.,'Login')]"

    # ---------------- Actions ----------------
    def setClientid(self, client_id: str):
        self.helper.enter_text(self.textbox_clientid_xpath, client_id, "Client ID")


    def setUserName(self, username: str):
        self.helper.enter_text(self.textbox_username_xpath, username, "Username")


    def setPassword(self, password: str):
        self.helper.enter_text(self.textbox_password_xpath, password, "Password")


    def clickLogin(self):
        self.helper.click(self.button_login_xpath, "Login button")


