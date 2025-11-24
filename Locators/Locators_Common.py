from playwright.sync_api import Page
from Utilities.BaseHelpers import BaseHelper

class Common_Locators:

    def __init__(self, page: Page):
        self.page = page
        self.helper = BaseHelper(page)

        # 🔹 Navigation Menu
        # Sidebar link to open the Admin section
        self.side_nav_admin = page.get_by_role("link", name="Admin")
        # Sidebar link to open the Lookups section
        self.side_nav_lookup = page.get_by_role("link", name="Lookups")


    # Admin Page Navigation Method
    def navigate_to_admin(self):
        self.helper.click(self.side_nav_admin, "Admin-side navigation link")

    def navigate_to_lookup(self):
        self.helper.click(self.side_nav_lookup, "Lookup-side navigation link")
