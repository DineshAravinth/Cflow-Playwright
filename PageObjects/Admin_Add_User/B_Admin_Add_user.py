from playwright.sync_api import Page, Locator, TimeoutError as PlaywrightTimeoutError
from Utilities.BaseHelpers import BaseHelper
from Locators.Locators_Admin_Add_User import Admin_Add_User_Locators
from Locators.Locators_Common import Common_Locators
import pandas as pd
from playwright.sync_api import expect
import random
import string
import re
import pytest
import time


class AdminNavigationAndAddUser:
    def __init__(self, page: Page, helper: BaseHelper):
        self.page = page
        self.helper = helper
        self.locators = Admin_Add_User_Locators(page)
        self.common = Common_Locators(page)

    # Navigate to Admin Page
    def go_to_admin(self):
        # Call the method from Common_Locators
        self.common.navigate_to_admin()

    # Click Add User button to add a new user
    def click_add_user(self):
        self.helper.click(self.locators.btn_add_user, "Add User button in the Admin page")

    # Generate a random string of lowercase letters
    @staticmethod
    def random_string(length=6):
        return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

    def enter_name(self, name=None):
        if not name:
            name = f"User_{self.random_string(5)}"
        self.helper.enter_text(self.locators.txt_name, name, "Name textbox")
        return name

    # Enter Department name
    def enter_department(self, dept):
        self.helper.enter_text(self.locators.txt_department, dept, "Department textbox")

    # Generate a random email address
    @staticmethod
    def random_email():
        return f"{AdminNavigationAndAddUser.random_string(6)}@yopmail.com"

    def enter_email(self, email=None):
        if not email:
            email = self.random_email()

        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            print(f"❌ Invalid email format: '{email}'")
            pytest.fail(f"Invalid Email Format: {email}", pytrace=False)

        self.helper.enter_text(self.locators.txt_email, email, "Email textbox")

    # Generate a random Login ID
    @staticmethod
    def random_login_id():
        return f"user_{AdminNavigationAndAddUser.random_string(5)}"

    def enter_login_id(self, login_id=None):
        if not login_id:
            login_id = self.random_login_id()

        print(f"🔑 Entering Login ID: {login_id}")
        self.helper.enter_text(self.locators.txt_login_id, login_id, "Login ID textbox")
        print(f"✅ Login ID entered successfully: {login_id}")
        return login_id

    # Generate an Employee Number
    @staticmethod
    def random_employee_number():
        return str(random.randint(1000, 9999))

    def enter_employee_number(self, emp_no=None):
        if not emp_no:
            emp_no = self.random_employee_number()
        self.helper.enter_text(self.locators.txt_employee_number, emp_no, "Employee Number textbox")
        return emp_no

    # Select Roles from dropdown
    def select_role(self, roles):
        if isinstance(roles, str):
            roles = [roles]

        print(f"🎯 Selecting roles: {roles}")

        for role in roles:
            print(f"➡ Selecting role: '{role}'")

            # Step 1️⃣ - Open dropdown before *each* selection
            self.helper.click(self.locators.dropdown_role, "Roles dropdown")
            self.page.wait_for_timeout(500)

            # Step 2️⃣ - Wait for dropdown to appear
            try:
                self.page.wait_for_selector("//div[@role='listbox']", state="visible", timeout=5000)
            except Exception:
                self.helper.take_screenshot(prefix="DropdownNotVisible")
                pytest.fail("❌ Role dropdown not visible after clicking")

            # Step 3️⃣ - Find and click the role
            role_option_xpath = f"//span[contains(@class,'ng-option-label') and normalize-space(text())='{role}']"
            role_option = self.page.locator(role_option_xpath)

            try:
                self.page.wait_for_selector(role_option_xpath, state="visible", timeout=5000)
                role_option.first.click()
                print(f"✅ Selected role: '{role}'")
            except Exception as e:
                self.helper.take_screenshot(prefix=f"ErrorSelecting_{role}")
                print(f"❌ Error selecting role '{role}': {e}")

                # Debug dropdown content if fails
                dropdown_texts = self.page.locator("//div[@role='listbox']").all_inner_texts()
                print(f"🧾 Dropdown visible options: {dropdown_texts}")

                pytest.fail(f"❌ Failed to select role '{role}': {e}")

            # Step 4️⃣ - Small delay for safety
            self.page.wait_for_timeout(500)

    # Generate whatsapp number with country code
    def enter_whatsapp_number(self, country_code="91", whatsapp_no="9876543210"):
        self.helper.enter_text(self.locators.country_code_input, country_code, "Country code input")
        self.helper.enter_text(self.locators.whatsapp_input, whatsapp_no, "WhatsApp number input")


    # Enable 'Send welcome mail to the user?' toggle
    def enable_send_welcome_mail(self):
        container = self.locators.send_welcome_mail_container
        checkbox = self.locators.send_welcome_mail_checkbox
        slider = self.locators.send_welcome_mail_slider

        container.wait_for(state="visible", timeout=5000)
        self.helper.scroll_to_label(container, "'Send welcome mail to the user?' toggle")

        try:
            is_checked = checkbox.evaluate("el => el.checked")
            if not is_checked:
                slider.click(force=True)
                self.page.wait_for_timeout(300)

            is_checked = checkbox.evaluate("el => el.checked")
            if is_checked:
                print("✔ 'Send welcome mail to the user?' toggle enabled")
            else:
                print("❌ Failed to enable 'Send welcome mail to the user?' toggle")
                self.helper.take_screenshot(prefix="SendWelcomeMailFailed")
        except Exception as e:
            print(f"❌ Error while enabling toggle: {e}")
            self.helper.take_screenshot(prefix="SendWelcomeMailError")

    # disable 'Status' toggle
    def disable_user_status_toggle(self):
        container = self.locators.user_status_container
        checkbox = self.locators.user_status_checkbox
        slider = self.locators.user_status_slider

        container.wait_for(state="visible", timeout=5000)
        self.helper.scroll_to_label(container, "'Status' toggle")

        try:
            is_checked = checkbox.evaluate("el => el.checked")

            if is_checked:
                slider.click(force=True)
                self.page.wait_for_timeout(300)

            is_checked = checkbox.evaluate("el => el.checked")
            if not is_checked:
                print("✔ 'Status' toggle disabled")
            else:
                print("❌ Failed to disable 'Status' toggle")
                self.helper.take_screenshot(prefix="StatusToggleFailed")
        except Exception as e:
            print(f"❌ Error while disabling 'Status' toggle: {e}")
            self.helper.take_screenshot(prefix="StatusToggleError")

    # Click Reset Password link/icon
    def click_reset_password(self):
        """
        Clicks the reset password icon/link in the Admin page.
        """
        self.helper.click(
            self.locators.reset_password_link,
            "Reset Password icon/link"
        )

    # To Search User in Admin Page
    def search_user(self, username: str, timeout: int = 5000):
        try:
            print(f"\n 🔍  Searching for user '{username}' in the Active Users page...")
            self.locators.search_box.wait_for(state="visible", timeout=timeout)
            self.locators.search_box.fill("")  # clear old value
            self.locators.search_box.fill(username)  # type username
            self.page.keyboard.press("Enter")  # trigger search
            self.page.wait_for_timeout(1500)  # wait for list refresh
            print(f"✅ User '{username}' search completed.")
        except Exception as e:
            self.helper.take_screenshot(f"SearchUserFailed_{username}")
            error_msg = f"❌ Failed to search user '{username}': {e}"
            print(error_msg)
            raise AssertionError(error_msg)

    # Click User in All Users page to open user details
    def click_user_in_All_Users_page(self, username: str, description: str = "'All Users list'", timeout: int = 10000):
        try:
            user_locator = self.page.locator(
                f'//div[contains(@class,"admin-grid-item")]//p[normalize-space(text())="{username}"]'
            )
            user_locator.wait_for(state="visible", timeout=timeout)
            user_locator.click()
            print(f"✅ Clicked on user '{username}' in {description}.")
        except Exception as e:
            self.helper.take_screenshot(f"ClickUserFailed_{username}")
            error_msg = f"❌ Failed to click user '{username}' in {description}: {e}"
            print(error_msg)
            raise AssertionError(error_msg)

    # Click Save button and validate toast messages
    def click_save(self):
        """
        Clicks the Save button and validates toast messages.
        Ensures screenshot and proper failure logging for any invalid state.
        """
        self.helper.click(self.locators.btn_save, "Save button")

        # Toast locator: supports both div/span structures
        toast = self.page.locator("#toast-container div, #toast-container span").first

        try:
            # Wait for toast to appear (max 5 seconds)
            toast.wait_for(state="visible", timeout=5000)
            message = " ".join(toast.inner_text().strip().split())  # Normalize whitespace
            print(f"💬 Toast detected: '{message}'")

            # --- Duplicate or error validations ---
            if re.search(r"username\s*already\s*exists?", message, re.IGNORECASE):
                screenshot_path = self.helper.take_screenshot("DuplicateLoginID")
                pytest.fail(f"❌ Duplicate Login ID: {message}. Screenshot: {screenshot_path}", pytrace=False)

            elif re.search(r"employee\s*no\s*already\s*exists?", message, re.IGNORECASE):
                screenshot_path = self.helper.take_screenshot("DuplicateEmployeeNo")
                pytest.fail(f"❌ Duplicate Employee No: {message}. Screenshot: {screenshot_path}", pytrace=False)

            elif re.search(r"(error|invalid|failed)", message, re.IGNORECASE):
                screenshot_path = self.helper.take_screenshot("GenericErrorToast")
                pytest.fail(f"❌ Form submission failed: {message}. Screenshot: {screenshot_path}", pytrace=False)

            else:
                print(f"✅ Success message: {message}")

        except PlaywrightTimeoutError:
            print("⚠️ No toast appeared after clicking Save — checking Save button visibility...")
            if self.locators.btn_save.is_visible():
                screenshot_path = self.helper.take_screenshot("SaveButtonStillVisible")
                pytest.fail(f"❌ Save did not complete successfully. Screenshot: {screenshot_path}", pytrace=False)
            else:
                print("✅ Save action likely successful (button hidden, no toast detected).")

        except Exception as e:
            print(f"⚠️ Unexpected error while handling toast: {e}")
            screenshot_path = self.helper.take_screenshot("UnexpectedToastError")
            pytest.fail(f"⚠️ Unexpected error during Save: {e}. Screenshot: {screenshot_path}", pytrace=False)

    # Click 'All Users' radio button to view all users
    def click_All_Users_radio(self):
        """Clicks the 'All Users' radio button."""
        self.locators.radio_btn_all_users.click(force=True)

    # Click 'Active Users' radio button to view only active users
    def click_Active_Users_radio_(self):
        """Clicks the 'Active Users' radio button."""
        self.locators.radio_btn_active_users.click(force=True)


    # Click 'Update' button in Reset Password for the user
    def click_update(self):
        """
        Clicks the 'Update' button in the Reset Password dialog or section.
        """
        try:
            self.locators.btn_update.wait_for(state="visible", timeout=5000)
            self.helper.click(self.locators.btn_update, "Update button")
            print("✅ Clicked the 'Update' button successfully.")
        except Exception as e:
            self.helper.take_screenshot("ClickUpdateFailed")
            error_msg = f"❌ Failed to click 'Update' button: {e}"
            print(error_msg)
            raise AssertionError(error_msg)

class UserVerificationAndDuplicateEmpNOLoginChecks:

    def __init__(self, page: Page, helper: BaseHelper, admin_nav: AdminNavigationAndAddUser, ):
        self.page = page
        self.helper = helper
        self.locators = Admin_Add_User_Locators(page)
        self.admin_nav = admin_nav

    # Verify that the created user is displayed in the All Users list.
    def verify_user_in_all_users(self, username):
        """
        ✅ Searches for the user and verifies if it appears in the All Users list.
        Takes a screenshot and raises an AssertionError if not found.
        """

        # Step 1: Locate the user in the grid
        user_row = self.page.locator(
            f"//div[contains(@class, 'admin-grid-item')]//p[normalize-space()='{username}']"
        )
        try:
            user_row.wait_for(state="visible", timeout=5000)
            print(f"✅ User '{username}' found in All Users Page.")
        except PlaywrightTimeoutError:
            self.helper.take_screenshot(f"UserNotFound_{username}")
            error_msg = f"❌ User '{username}' not found in All Users list."
            print(error_msg)
            raise AssertionError(error_msg)

    # Verify whether the user's status toggle is enabled or disabled
    def verify_user_status_toggle(self, username: str, description: str = "'User Status Toggle'", timeout: int = 10000):
        """
        Verify whether the given user's status toggle is enabled (Active) or disabled (Inactive).
        """
        print(f"\n🔍  Verifying user status toggle for '{username}' under {description}...")
        try:
            toggle_locator = self.page.locator(
                f'//p[normalize-space()="{username}"]/ancestor::div[contains(@class,"admin-grid-item")]//input[@aria-label="User Status"]'
            )
            toggle_locator.wait_for(state="attached", timeout=timeout)
            is_checked = toggle_locator.is_checked()

            if is_checked:
                print(f"🔴 🏆  User '{username}' status is Active (toggle ON).")
                return "Active"
            else:
                print(f"🔴  User '{username}' status is Disabled (toggle OFF).")
                return "Disabled"
        except Exception as e:
            self.helper.take_screenshot(f"ToggleCheckFailed_{username}")
            error_msg = f"❌ Test failed — Unable to verify toggle for '{username}': {e}"
            print(error_msg)
            raise AssertionError(error_msg)

    # To verify that the user's status toggle is disabled
    def verify_user_status_toggle_disabled(self, username: str, description: str = "'User Status Toggle'",
                                           timeout: int = 10000):
        """
        Verify that the given user's status toggle is disabled (Inactive).
        Fails the test if the toggle is enabled (Active).
        """
        print(f"🔍  Verifying that user status toggle for '{username}' under {description} is DISABLED...")
        try:
            toggle_locator = self.page.locator(
                f'//p[normalize-space()="{username}"]/ancestor::div[contains(@class,"admin-grid-item")]//input[@aria-label="User Status"]'
            )
            toggle_locator.wait_for(state="attached", timeout=timeout)
            is_checked = toggle_locator.is_checked()

            if not is_checked:
                print(f"✔ User '{username}' status is Disabled (toggle OFF).")
                return "Disabled"
            else:
                error_msg = f"❌ User '{username}' status is Active (toggle ON) — expected Disabled."
                self.helper.take_screenshot(f"ToggleShouldBeDisabled_{username}")
                print(error_msg)
                raise AssertionError(error_msg)
        except Exception as e:
            self.helper.take_screenshot(f"ToggleCheckFailed_{username}")
            error_msg = f"❌ Test failed — Unable to verify toggle for '{username}': {e}"
            print(error_msg)
            raise AssertionError(error_msg)

    # Enable a disabled user's toggle (make them Active) and verify it.
    def enable_user_toggle(self, username: str, description: str = "'User Status Toggle'", timeout: int = 10000):
        """
        Enable a disabled user's toggle (make them Active) and verify it.
        Searches the user first to ensure visibility.
        """
        print(f"🟢 Enabling user status toggle for '{username}' under {description}...")

        try:
            # Step 1️⃣: Search for the user
            print(f"🔍 Searching for user '{username}' before enabling toggle...")
            search_box = self.page.locator("#search-user-grid-records")
            search_box.wait_for(state="visible", timeout=5000)
            search_box.fill("")  # clear old value
            search_box.fill(username)  # type username
            self.page.keyboard.press("Enter")  # trigger search
            self.page.wait_for_timeout(1500)  # wait for list refresh
            print(f"✅ User '{username}' search completed.")

            # Step 2️⃣: Locate the visible toggle (span)
            toggle_slider = self.page.locator(
                f'//p[normalize-space()="{username}"]/ancestor::div[contains(@class,"admin-grid-item")]'
                f'//label[@class="switch"]/span[@class="slider"]'
            )

            toggle_checkbox = self.page.locator(
                f'//p[normalize-space()="{username}"]/ancestor::div[contains(@class,"admin-grid-item")]'
                f'//input[@aria-label="User Status"]'
            )

            toggle_slider.wait_for(state="visible", timeout=timeout)

            # Step 3️⃣: Scroll into view
            try:
                self.helper.scroll_to_label(toggle_slider, friendly_name=f"{username} Toggle")
            except Exception as e:
                print(f"⚠ Scroll attempt failed or element already in view: {e}")

            # Step 4️⃣: Verify current state via checkbox
            is_checked = toggle_checkbox.is_checked()
            if is_checked:
                print(f"ℹ User '{username}' toggle is already enabled.")
                return "Already Enabled"

            # Step 5️⃣: Click the visible slider
            toggle_slider.click(force=True)
            print(f"🖱 Clicked visible toggle (slider) for '{username}'...")

            # ✅ Step 6️⃣: Handle the confirmation popup (Yes button)
            yes_button = self.page.locator(
                '//div[contains(@class,"war-pop-footer")]//button[contains(@class,"button-danger") and normalize-space(text())="Yes"]'
            )

            try:
                yes_button.wait_for(state="visible", timeout=5000)
                yes_button.scroll_into_view_if_needed()
                yes_button.click()
                print("🆗 Clicked 'Yes' button on confirmation popup.")
            except Exception:
                print("⚠ No confirmation popup detected, continuing...")

            # Wait a moment for UI update
            self.page.wait_for_timeout(1500)

            # Step 7️⃣: Confirm it’s enabled
            if toggle_checkbox.is_checked():
                print(f"✅ User '{username}' successfully enabled (toggle ON).")
                return "Enabled"
            else:
                self.helper.take_screenshot(f"EnableToggleFailed_{username}")
                error_msg = f"❌ User '{username}' toggle did not enable properly."
                print(error_msg)
                raise AssertionError(error_msg)

        except Exception as e:
            self.helper.take_screenshot(f"EnableToggleFailed_{username}")
            error_msg = f"❌ Test failed while enabling toggle for '{username}': {e}"
            print(error_msg)
            raise AssertionError(error_msg)

    # To verify that the created user is displayed in the Active Users list.
    def verify_user_in_Active_List(self, username: str, timeout: int = 10000):
        """
        Switches to Active Users tab and verifies that the user appears there.
        """
        print(f"👁️  Checking if '{username}' appears in Active Users list...")
        self.admin_nav.click_Active_Users_radio_()
        self.page.wait_for_timeout(2000)

        user_locator = self.page.locator(f'//p[normalize-space()="{username}"]')
        try:
            user_locator.wait_for(state="visible", timeout=timeout)
            print(f"✅ User '{username}' is displayed in Active Users list.")
            return True
        except:
            self.helper.take_screenshot(f"UserNotFoundInActive_{username}")
            raise AssertionError(f"❌ User '{username}' not found in Active Users list.")

    # To verify duplicate login toast message
    def verify_duplicate_login_toast(self, expected_message: str):
        """
        Click Save and check if expected duplicate login toast appears.
        Takes screenshot if toast does not appear or message mismatch.
        """
        self.helper.click(self.locators.btn_save, "Save button")

        try:
            # Wait for toast container to attach
            self.page.locator("#toast-container").wait_for(state="attached", timeout=5000)

            # Wait for the actual toast message
            toast_locator = self.page.locator("#toast-container div, #toast-container span").first
            toast_locator.wait_for(state="visible", timeout=10000)

            message = " ".join(toast_locator.inner_text().strip().split())
            print(f"⚠️ Toast message detected: {message}")

            if expected_message.lower() not in message.lower():
                self.helper.take_screenshot(prefix="DuplicateToastMismatch")
                error_msg = f"❌ Expected message '{expected_message}', but got: '{message}'"
                print(error_msg)
                raise AssertionError(error_msg)

            print("✅ Negative test passed: Toast message displayed correctly")
            return True

        except PlaywrightTimeoutError:
            print("⚠️ Toast did not appear — taking screenshot.")
            self.helper.take_screenshot(prefix="ToastNotFound")
            error_msg = f"❌ Expected toast message '{expected_message}' did not appear"
            print(error_msg)
            raise AssertionError(error_msg)

        except Exception as e:
            self.helper.take_screenshot(prefix="DuplicateToastError")
            error_msg = f"❌ Unexpected error while verifying duplicate login toast: {e}"
            print(error_msg)
            raise AssertionError(error_msg)

    # To verify duplicate Employee No toast message
    def verify_duplicate_emp_toast(self):
        """
        Click Save and verify 'Employee No Already Exist' toast appears.
        Takes screenshot if toast does not appear or message mismatch.
        """
        self.helper.click(self.locators.btn_save, "Save button")

        try:
            self.page.locator("#toast-container").wait_for(state="attached", timeout=5000)

            toast_locator = self.page.locator("#toast-container div, #toast-container span").first
            toast_locator.wait_for(state="visible", timeout=10000)

            message = " ".join(toast_locator.inner_text().strip().split())
            print(f"⚠️ Toast message detected: {message}")

            if "Employee No Already Exist" not in message:
                self.helper.take_screenshot(prefix="DuplicateEmpToastMismatch")
                error_msg = f"❌ Expected duplicate employee number message, but got: '{message}'"
                print(error_msg)
                raise AssertionError(error_msg)

            print("✅ Negative test passed: Duplicate Employee Number message displayed correctly")

        except PlaywrightTimeoutError:
            print("⚠️ Toast did not appear — taking screenshot.")
            self.helper.take_screenshot(prefix="DuplicateEmpToastNotFound")
            error_msg = "❌ Expected duplicate Employee Number toast did not appear"
            print(error_msg)
            raise AssertionError(error_msg)

        except Exception as e:
            self.helper.take_screenshot(prefix="DuplicateEmpToastError")
            error_msg = f"❌ Unexpected error while verifying duplicate employee toast: {e}"
            print(error_msg)
            raise AssertionError(error_msg)

class PasswordGenerationAndValidation:
    """
    Handles password entry, policy validation, generation, and reset flows.
    """
    def __init__(self, page: Page, helper: BaseHelper):
        self.page = page
        self.helper = helper
        self.locators = Admin_Add_User_Locators(page)
        self.current_password: str | None = None  # Stores last used password for reuse

        # Primary locators
        self.txt_password: Locator = self.locators.txt_password
        self.btn_update: Locator = self.locators.btn_update

    # ------------------- Password Entry -------------------
    def enter_password(self, password: str | None = None) -> str:
        """
        Enters a password. If not provided, dynamically generates a valid one.
        Returns the final password.
        """
        if not password:
            password = self.generate_valid_password()
        self.helper.enter_text(self.txt_password, password, "Password textbox")
        return password

    def enter_new_password(self, password: str):
        """
        Enters a new password into the Reset Password form.
        """
        try:
            new_password_field = self.page.locator(
                "//input[@type='password' and @name='reset=password-user']"
            )
            new_password_field.wait_for(state="visible", timeout=5000)
            self.helper.enter_text(new_password_field, password, "Reset Password field")
        except Exception as e:
            self.helper.take_screenshot("EnterNewPasswordFailed")
            raise AssertionError(f"❌ Failed to enter new password: {e}")

    # ------------------- Password Policy Helpers -------------------
    def get_visible_password_rules(self) -> list[str]:
        """
        Returns all currently visible password rules.
        """
        field = self.txt_password
        field.fill("a")  # trigger validation container
        self.page.wait_for_timeout(200)

        rules_locator: Locator = self.page.locator("cf-password-policy-validate .password-validation ul li")
        visible_rules: list[str] = [rules_locator.nth(i).inner_text().strip()
                                    for i in range(rules_locator.count()) if rules_locator.nth(i).is_visible()]

        field.fill("")  # Clear temporary char
        if visible_rules:
            print("🔍 Visible password validations:")
            for idx, rule in enumerate(visible_rules, 1):
                print(f"{idx}. {rule}")
        else:
            print("✅ No visible password validations.")
        return visible_rules

    @staticmethod
    def parse_length_limits(rules: list[str]) -> tuple[int, int]:
        """
        Parses min and max length from visible rules.
        """
        min_len, max_len = 8, 20
        for rule in rules:
            r_lower = rule.lower()
            if "at least" in r_lower:
                min_len = max(min_len, int(''.join(filter(str.isdigit, rule))))
            elif "less than" in r_lower:
                max_len = min(max_len, int(''.join(filter(str.isdigit, rule))) - 1)
        return min_len, max_len

    @staticmethod
    def add_char_for_rule(rules: list[str]) -> str:
        """
        Returns a character that satisfies one of the unmet rules.
        """
        for rule in rules:
            r_lower = rule.lower()
            if "number" in r_lower:
                return random.choice(string.digits)
            if "uppercase" in r_lower:
                return random.choice(string.ascii_uppercase)
            if "alphabet" in r_lower:
                return random.choice(string.ascii_lowercase)
            if "special" in r_lower:
                return random.choice("!@#$%^&*")
            if "at least" in r_lower or "less than" in r_lower:
                return random.choice(string.ascii_letters + string.digits + "!@#$%^&*")
        return random.choice(string.ascii_letters + string.digits + "!@#$%^&*")


    def _rule_satisfied(self, rule: str, password: str) -> bool:
        """
        Checks if password satisfies a single rule.
        """
        r_lower = rule.lower()
        if "number" in r_lower:
            return any(c.isdigit() for c in password)
        if "uppercase" in r_lower:
            return any(c.isupper() for c in password)
        if "alphabet" in r_lower:
            return any(c.islower() for c in password)
        if "special" in r_lower:
            return any(c in "!@#$%^&*" for c in password)
        if "at least" in r_lower:
            min_len = int(''.join(filter(str.isdigit, rule)))
            return len(password) >= min_len
        if "less than" in r_lower:
            max_len = int(''.join(filter(str.isdigit, rule))) - 1
            return len(password) <= max_len
        return True

    def generate_valid_password(self) -> str:
        """
        Generates a valid password based on visible rules.
        """
        password = ""
        visible_rules = self.get_visible_password_rules()
        min_len, max_len = self.parse_length_limits(visible_rules)

        # Satisfy all rules
        while True:
            unmet_rules = [rule for rule in visible_rules if not self._rule_satisfied(rule, password)]
            if not unmet_rules or len(password) >= max_len:
                break
            password += self.add_char_for_rule(unmet_rules)
            self.txt_password.fill(password)
            time.sleep(0.05)

        # Ensure minimum length
        while len(password) < min_len:
            password += random.choice(string.ascii_letters + string.digits + "!@#$%^&*")
            self.txt_password.fill(password)
            time.sleep(0.02)

        print(f"🔑 Generated valid password: {password}")
        return password

    # ------------------- Reset Password Flow -------------------
    def reset_password_with_policy_check(self, old_password: str | None = None) -> str:
        """
        Resets user password:
          1. Click reset link
          2. Enter old password (expect policy fail toast)
          3. Generate and enter new valid password
          4. Click Update, validate success toast
        Returns new password.
        """
        if not old_password:
            if self.current_password:
                old_password = self.current_password
            else:
                raise ValueError("No old password available. Pass one or set current_password.")

        # Step 1: Click reset password
        self.helper.click(self.locators.reset_password_link, "Reset Password link")

        # Step 2: Enter old password (expect failure)
        print(f"🧪 Trying old password: {old_password}")
        self.enter_new_password(old_password)
        self.helper.click(self.btn_update, "Update button (old password)")

        # Step 2a: Verify policy toast
        toast = self.page.locator("#toast-container div, #toast-container span").first
        try:
            toast.wait_for(state="visible", timeout=5000)
            message = toast.inner_text().strip()
            if "not met" in message.lower() or "policy" in message.lower():
                print(f"✅ Policy validation triggered correctly: '{message}'")
            else:
                self.helper.take_screenshot("UnexpectedToast_ResetPassword")
                pytest.fail(f"❌ Unexpected toast after old password: {message}", pytrace=False)
        except PlaywrightTimeoutError:
            self.helper.take_screenshot("NoToast_ResetPassword")
            pytest.fail("❌ No toast appeared after old password attempt.", pytrace=False)

        # Step 3: Generate new valid password
        new_password = self.generate_valid_password()
        self.enter_new_password(new_password)

        # Step 4: Click update for new password
        self.helper.click(self.btn_update, "Update button (valid password)")
        self.page.wait_for_timeout(3000)

        # Step 4a: Verify success toast
        try:
            toast.wait_for(state="visible", timeout=5000)
            message = toast.inner_text().strip()
            if "password updated successfully" in message.lower():
                print(f"✅ Password reset successful: '{message}'")
            else:
                self.helper.take_screenshot("UnexpectedToast_NewPassword")
                pytest.fail(f"❌ Unexpected toast after new password: {message}", pytrace=False)
        except PlaywrightTimeoutError:
            self.helper.take_screenshot("NoToast_NewPassword")
            pytest.fail("❌ No toast appeared after updating new password.", pytrace=False)

        self.current_password = new_password
        return new_password


# ---------------- Password Utilities ----------------
class PasswordUtils:
    @staticmethod
    def parse_length_limits(rules: list[str]) -> tuple[int, int]:
        """
        Parse minimum and maximum length dynamically from visible rules.
        """
        min_len = 8
        max_len = 20
        for rule in rules:
            r_lower = rule.lower()
            if "at least" in r_lower:
                min_len = max(min_len, int(''.join(filter(str.isdigit, rule))))
            elif "less than" in r_lower:
                max_len = min(max_len, int(''.join(filter(str.isdigit, rule))) - 1)
        return min_len, max_len

# ---------------- Invalid Password Tests ----------------
class InvalidPasswordTests:
    def __init__(self, page: Page, helper: BaseHelper, txt_password_locator, btn_save_locator):
        self.page = page
        self.helper = helper
        self.txt_password = txt_password_locator
        self.btn_save = btn_save_locator

    def generate_invalid_passwords(self) -> list[tuple[str, str]]:
        """
        Dynamically generates invalid passwords for each visible validation rule.
        Returns a list of tuples (rule_text, invalid_password).
        """
        field = self.txt_password

        # Trigger container by typing a character
        field.fill("a")
        self.page.wait_for_timeout(300)

        rules = self.page.locator("cf-password-policy-validate .password-validation ul li")
        invalid_passwords: list[tuple[str, str]] = []

        count = rules.count()
        if count == 0:
            print("✅ No visible password validations found — skipping invalid password generation.")
            return []

        # Collect visible rules
        visible_rules: list[str] = []
        for i in range(count):
            r = rules.nth(i)
            if r.is_visible():
                visible_rules.append(r.inner_text().strip())

        print(f"\n🔍 Found {len(visible_rules)} visible password rules:")
        for idx, rule in enumerate(visible_rules, start=1):
            print(f"   {idx}. {rule}")

        # Determine min and max from current rules
        min_len, max_len = PasswordUtils.parse_length_limits(visible_rules)

        # Generate invalid passwords for each rule
        for rule in visible_rules:
            rule_lower = rule.lower()
            invalid_pwd = ""

            if "at least" in rule_lower:
                target_len = max(1, min_len - 1)
                invalid_pwd = ''.join(random.choices(string.ascii_letters + string.digits + "!@#$%^&*", k=target_len))

            elif "less than" in rule_lower:
                target_len = max_len + 3
                invalid_pwd = ''.join(random.choices(string.ascii_letters + string.digits + "!@#$%^&*", k=target_len))

            elif "number" in rule_lower:
                target_len = max(min_len, 8)
                invalid_pwd = ''.join(random.choices(string.ascii_letters + "!@#$%^&*", k=target_len))

            elif "uppercase" in rule_lower:
                target_len = max(min_len, 8)
                invalid_pwd = ''.join(random.choices(string.ascii_lowercase + string.digits + "!@#$%^&*", k=target_len))

            elif "alphabet" in rule_lower:
                target_len = max(min_len, 8)
                invalid_pwd = ''.join(random.choices(string.digits + "!@#$%^&*", k=target_len))


            elif "special" in rule_lower:
                target_len = max(min_len, 8)
                invalid_pwd = random.choice(string.digits) + ''.join(
                    random.choices(string.ascii_letters + string.digits, k=target_len - 1)
                )

            else:
                target_len = max(1, min_len - 1)
                invalid_pwd = ''.join(random.choices(string.ascii_letters + string.digits + "!@#$%^&*", k=target_len))

            print(f"   -> Rule: '{rule}' -> invalid password length: {len(invalid_pwd)} -> pwd: {invalid_pwd}")
            invalid_passwords.append((rule, invalid_pwd))

        return invalid_passwords

    def test_invalid_passwords(self):
        """
        Loops through each invalid password, fills it,
        clicks 'Save', and checks that the Save button is still visible.
        Fails the test if an invalid password is accepted.
        """
        invalid_passwords = self.generate_invalid_passwords()

        if not invalid_passwords:
            print("✅ No password rules found — skipping invalid tests.")
            return

        for rule, bad_pwd in invalid_passwords:
            print(f"\n🧩 Testing invalid password for rule: {rule}")
            print(f"   ➡ Invalid password used: {bad_pwd} (len={len(bad_pwd)})")

            # Clear and type password
            self.txt_password.fill("")
            self.page.wait_for_timeout(500)
            self.txt_password.fill(bad_pwd)

            # Wait for frontend validation to update
            self.page.wait_for_timeout(1000)

            # Click Save
            self.helper.click(self.btn_save, "Save button")
            self.page.wait_for_timeout(1000)

            try:
                if self.btn_save.is_visible():
                    print(f"✅ Negative case passed — Save button still visible for rule: '{rule}'")
                else:
                    screenshot_name = f"InvalidPassword_{re.sub(r'[^0-9a-zA-Z]+', '_', rule)[:30]}"
                    self.helper.take_screenshot(screenshot_name)
                    pytest.fail(f"❌ Invalid password accepted for rule '{rule}'. Screenshot: {screenshot_name}",
                                pytrace=False)

            except Exception:
                screenshot_name = f"CheckSaveVisibleError_{re.sub(r'[^0-9a-zA-Z]+', '_', rule)[:30]}"
                self.helper.take_screenshot(screenshot_name)
                pytest.fail(
                    f"⚠️ Exception while verifying Save button for rule '{rule}'. Screenshot: {screenshot_name}",
                    pytrace=False)

            self.page.wait_for_timeout(1000)

    @staticmethod
    def _rule_satisfied(rule: str, password: str) -> bool:
        """
        Checks if a password satisfies a single rule.
        """
        r_lower = rule.lower()
        if "number" in r_lower:
            return any(c.isdigit() for c in password)
        if "uppercase" in r_lower:
            return any(c.isupper() for c in password)
        if "alphabet" in r_lower:
            return any(c.islower() for c in password)
        if "special" in r_lower:
            return any(c in "!@#$%^&*" for c in password)
        if "at least" in r_lower:
            min_len = int(''.join(filter(str.isdigit, rule)))
            return len(password) >= min_len
        if "less than" in r_lower:
            max_len = int(''.join(filter(str.isdigit, rule))) - 1
            return len(password) <= max_len
        return True

class VerifyUserInEmployeesLookup:

    # Centralized locators
    MENU_EMPLOYEE_LOOKUP = "//span[normalize-space()='Employee Lookup']"
    TABLE_FIRST_ROW = "//table//tbody/tr[1]"

    def __init__(self, page: Page, helper: BaseHelper):
        self.page = page
        self.helper = helper
        self.locators = Admin_Add_User_Locators(page)
        self.common = Common_Locators(page)

    # Navigate to Lookup Page
    def go_to_lookup(self):
        # Call the method from Common_Locators
        self.common.navigate_to_lookup()

    # Click Employees Lookup
    def employees_lookup(self):
        self.helper.click(self.locators.click_employees_lookup, "Employees Lookup")

    # Verify latest employee record
    def verify_latest_employee_record(self, expected_data: dict):
        print("🧭 Fetching latest employee record from lookup table...")

        # Wait until the first row is visible
        self.page.wait_for_selector(self.TABLE_FIRST_ROW)
        latest_row = self.page.locator(self.TABLE_FIRST_ROW)

        # Extract all useful details (adjust td index if table structure differs)
        actual_data = {
            "ID": latest_row.locator("td:nth-child(3)").inner_text().strip(),
            "Employee No": latest_row.locator("td:nth-child(4)").inner_text().strip(),
            "Employee Name": latest_row.locator("td:nth-child(5)").inner_text().strip(),
            "Login ID": latest_row.locator("td:nth-child(6)").inner_text().strip(),
            "Email ID": latest_row.locator("td:nth-child(7)").inner_text().strip(),
            "Department": latest_row.locator("td:nth-child(8)").inner_text().strip(),
            "Created By": latest_row.locator("td:nth-child(9)").inner_text().strip(),
            "Created Date": latest_row.locator("td:nth-child(10)").inner_text().strip(),
            "Updated By": latest_row.locator("td:nth-child(11)").inner_text().strip(),
            "Updated Date": latest_row.locator("td:nth-child(12)").inner_text().strip(),
        }

        # Print the complete record
        print("\n🧾 Employee Record (Full Details):")
        for key, value in actual_data.items():
            print(f"   {key}: {value}")

        # Compare only required fields
        print("\n📊 Comparing Employee Record Details:")
        for key, expected_value in expected_data.items():
            actual_value = actual_data.get(key)
            if actual_value != expected_value:
                self.helper.take_screenshot(prefix=f"Mismatch_{key}")
                print(f"❌ {key}: Expected '{expected_value}', Got '{actual_value}'")
                raise AssertionError(
                    f"Mismatch in '{key}': expected '{expected_value}', got '{actual_value}'"
                )
            else:
                print(f"✅ {key} matches: '{actual_value}'")

        print("\n🎯 All employee details correctly reflected in Employee Lookup table.")

class ImportUserFromExcel:

    def __init__(self, page: Page, helper: BaseHelper):
        self.page = page
        self.helper = helper
        self.locators = Admin_Add_User_Locators(page)
        self.common = Common_Locators(page)

    # To Import the users
    def click_import(self):
        self.helper.click(self.locators.btn_import, "Import button on the page")

    # To upload a file
    def upload_file(self, file_path):
        self.helper.upload_file(self.locators.input_upload_file, file_path, "Excel file upload field")

    # To click the upload button
    def click_upload(self):
        """
        Clicks the Upload button and validates success, error, or duplicate user popups.
        Handles SweetAlert2 (swal2) info dialogs, toast messages, and ensures proper assertions.
        Checks toast message first, then validates Import Summary popup if it appears.
        """
        self.helper.click(self.locators.btn_upload, "Upload button")

        # --- Step 1: Check for Toast message first ---
        # --- Step 1: Check for Toast message first ---
        toast = self.page.locator("#toast-container div, #toast-container span").first

        try:
            toast.wait_for(state="visible", timeout=8000)
            message = " ".join(toast.inner_text().strip().split())
            print(f"💬 Toast detected after upload: '{message}'")

            # --- Handle toast types ---
            if re.search(r"(error|failed|invalid)", message, re.IGNORECASE):
                screenshot_path = self.helper.take_screenshot("UploadErrorToast")
                pytest.fail(f"❌ Upload failed: {message}. Screenshot: {screenshot_path}", pytrace=False)

            elif re.search(r"already\s*exists|duplicate", message, re.IGNORECASE):
                screenshot_path = self.helper.take_screenshot("UploadDuplicateToast")
                pytest.fail(f"⚠️ Duplicate data found: {message}. Screenshot: {screenshot_path}", pytrace=False)

            elif re.search(r"success|imported\s*\d+\s*users?", message, re.IGNORECASE):
                print(f"✅ Upload successful based on toast: {message}")
                # ✅ No screenshot needed for success

            else:
                screenshot_path = self.helper.take_screenshot("UploadUnknownToast")
                pytest.fail(f"⚠️ Unexpected toast message: {message}. Screenshot: {screenshot_path}", pytrace=False)

        except PlaywrightTimeoutError:
            # ✅ No toast appeared — treat as success without further checks
            print("ℹ️ No toast appeared after clicking Upload.")

        except Exception as e:
            print(f"⚠️ Unexpected error while handling upload toast: {e}")
            screenshot_path = self.helper.take_screenshot("UnexpectedUploadToastError")
            pytest.fail(f"⚠️ Unexpected error during toast validation: {e}. Screenshot: {screenshot_path}",
                        pytrace=False)
        # --- Step 2: Handle Import Summary popup (if shown) ---
        popup = self.page.locator('//div[contains(@class,"swal2-popup") and contains(@class,"swal2-show")]')
        popup_html_container = self.page.locator('//div[@id="swal2-html-container"]').first
        popup_ok_button = self.page.locator('//button[contains(@class,"swal2-confirm")]')

        try:
            popup.wait_for(state="visible", timeout=5000)
            print("✅ SweetAlert2 Import Summary popup appeared.")

            raw_html = popup_html_container.inner_html().strip()
            clean_text = re.sub(r"<[^>]+>", "", raw_html)
            clean_text = " ".join(clean_text.split())
            print(f"ℹ️ Popup text detected: {clean_text}")

            screenshot_path = self.helper.take_screenshot("ImportSummaryPopup")

            # --- Validate Import Summary ---
            if re.search(r"import\s+summary", clean_text, re.IGNORECASE):
                print(f"✅ Import Summary detected: {clean_text}")

                if re.search(r"found\s+\d+\s+existing\s+user", clean_text, re.IGNORECASE):
                    pytest.fail(
                        f"❌ Import Summary indicates existing user(s): {clean_text}. "
                        f"Screenshot: {screenshot_path}",
                        pytrace=False
                    )
                else:
                    print("🎉 Import Summary confirmed without existing users.")
            else:
                pytest.fail(
                    f"⚠️ Unexpected popup content: {clean_text}. Screenshot: {screenshot_path}",
                    pytrace=False
                )



        except PlaywrightTimeoutError:
            print("ℹ️ No 'Import Summary' popup detected — continuing...")

        except Exception as e:
            print(f"⚠️ Error while handling 'Import Summary' popup: {e}")
            self.helper.take_screenshot("PopupHandlingError")

    def verify_imported_users_from_excel(self, excel_path: str):
        """
        Verifies each imported user's details from Excel against the data in the application.
        Uses existing locators for field validation (name, email, login ID, etc.)
        """
        try:
            df = pd.read_excel(excel_path)
            print(f"📄 Loaded {len(df)} users from Excel for verification.\n")

            for index, row in df.iterrows():
                name = str(row["Name"]).strip()
                login_id = str(row["Login ID"]).strip()
                email = str(row["Email"]).strip()
                role = str(row["Role"]).strip()
                whatsapp = str(row["WhatsApp Number"]).strip()
                emp_no = str(row["Employee Number"]).strip()
                dept = str(row["Department"]).strip()

                print(f"🔍 Verifying imported user: {name}")

                # Step 1️⃣: Search user
                search_box = self.page.locator('//input[@id="search-user-grid-records"]')
                search_box.wait_for(state="visible", timeout=5000)
                search_box.fill(name)
                self.page.keyboard.press("Enter")
                self.page.wait_for_timeout(2000)

                # Step 2️⃣: Open user record
                user_card = self.page.locator(f'//p[normalize-space()="{name}"]')
                expect(user_card).to_be_visible(timeout=5000)
                user_card.click()
                self.page.wait_for_timeout(2000)

                # Step 3️⃣: Validate form fields
                field_map = {
                    "Name": self.locators.txt_name,
                    "Login ID": self.locators.txt_login_id,
                    "Email": self.locators.txt_email,
                    "Role": self.locators.verify_role,
                    "WhatsApp Number": self.locators.whatsapp_input,
                    "Employee Number": self.locators.txt_employee_number,
                    "Department": self.locators.txt_department,
                }

                expected_values = {
                    "Name": name,
                    "Login ID": login_id,
                    "Email": email,
                    "Role": role,
                    "WhatsApp Number": whatsapp,
                    "Employee Number": emp_no,
                    "Department": dept,
                }

                for label, locator in field_map.items():
                    try:
                        locator.wait_for(state="visible", timeout=5000)

                        # Try to get value intelligently
                        tag_name = locator.evaluate("el => el.tagName.toLowerCase()")
                        actual_value = ""

                        if tag_name == "input" or tag_name == "textarea":
                            actual_value = locator.input_value().strip()
                        else:
                            # For ng-select, span, div, or any wrapper element
                            try:
                                actual_value = locator.inner_text().strip()
                            except Exception:
                                actual_value = locator.text_content().strip()

                        expected_value = expected_values[label]
                        if actual_value != expected_value:
                            screenshot = self.helper.take_screenshot(f"Mismatch_{login_id}_{label}")
                            raise AssertionError(
                                f"❌ {label} mismatch for {login_id}: "
                                f"Expected '{expected_value}', Found '{actual_value}'. Screenshot: {screenshot}"
                            )

                        print(f"✅ {label} matches: {actual_value}")

                    except Exception as e:
                        screenshot = self.helper.take_screenshot(f"VerifyFieldError_{login_id}_{label}")
                        raise AssertionError(f"❌ Error verifying {label} for {login_id}: {e}. Screenshot: {screenshot}")

                print(f"🎯 Verification completed for '{name}'\n")

                # Step 4️⃣: Go back to list
                back_button = self.page.locator("//a[@aria-label='Close']")
                if back_button.is_visible():
                    back_button.click()
                    self.page.wait_for_timeout(1500)

            print("✅ All imported users verified successfully!")

        except Exception as e:
            screenshot_path = self.helper.take_screenshot("VerifyImportedUsersFailed")
            raise AssertionError(f"❌ Failed to verify imported users: {e}. Screenshot: {screenshot_path}")



class NewUserLoginVerification:
    """
    Verifies that a newly created user can log in.
    Uses BaseHelper for actions and verification.
    """
    def __init__(self, page: Page, login_url: str):
        self.page = page
        self.login_url = login_url
        self.helper = BaseHelper(page)

        # Locators
        self.textbox_clientid_xpath = '//*[@id="client-id"]'
        self.textbox_username_xpath = '//*[@id="username"]'
        self.textbox_password_xpath = '//*[@id="password"]'
        self.button_login_xpath = "//button[contains(.,'Login')]"

    def verify_new_user_login(self, client_id: str, login_id: str, password: str, username: str):
        print(f"\n🔐 Verifying login for new user: {username}")

        # Navigate to login page
        self.page.goto(self.login_url)

        # Fill login form using BaseHelper
        self.helper.enter_text(self.textbox_clientid_xpath, client_id, "Client ID")
        self.helper.enter_text(self.textbox_username_xpath, login_id, "Login ID")
        self.helper.enter_text(self.textbox_password_xpath, password, "Password")

        # Click login
        self.helper.click(self.button_login_xpath, "Login button")
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(5000)

        # Validate login success
        try:
            expected_fragment = "/dashboard"
            if expected_fragment.lower() not in self.page.url.lower():
                raise AssertionError(f"Current URL: {self.page.url}")
            print(f"✅ Login successful for user: {username}")

        except Exception as e:
            self.helper.take_screenshot(f"LoginFailed_{username}")
            pytest.fail(f"❌ Login failed for user '{username}': {e}", pytrace=False)
