from playwright.sync_api import Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
import random
import string
import re
import pytest
from Utilities.BaseHelpers import BaseHelper
import time
from playwright.sync_api import Locator

class Admin_Add_User:
    def __init__(self, page: Page, timeout: int = 30):
        self.page = page
        self.timeout = timeout
        self.helper = BaseHelper(page)

        # ---------------- Locators ----------------
        self.side_nav_admin = page.get_by_role("link", name="Admin")
        self.btn_add_user = page.get_by_role("button", name="Add User")
        self.txt_name = page.locator('input[formcontrolname="name"]')
        self.txt_department = page.locator('input[formcontrolname="department"]')
        self.txt_email = page.locator('input[formcontrolname="email"]')
        self.txt_login_id = page.locator('input[formcontrolname="loginId"]')
        self.txt_password = page.locator('input[formcontrolname="password"]')
        self.txt_employee_number = page.locator('input[formcontrolname="empNo"]')
        self.dropdown_role = page.locator('ng-select[formcontrolname="role"]')
        self.label_locator = page.locator('//label[normalize-space(text())="Send welcome mail to the user?"]')
        self.toggle_send_mail = page.locator(
            "(//label[@id='flexCheckDefault' and contains(@class,'switch')]/span[@class='slider'])[2]"
        )
        self.btn_save = page.locator('//button[normalize-space(text())="Save"]')
        self.country_code_input = page.locator('//div[contains(@class, "d-flex")]/input[@placeholder="+91"]')
        self.whatsapp_input = page.locator('//div[contains(@class, "d-flex")]/input[@formcontrolname="whatsappNo"]')
        self.radio_btn_all_users = page.locator('//label[.//span[normalize-space()="All Users"]]')
        self.radio_btn_active_users = page.locator('//label[.//span[normalize-space()="Active Users"]]')
        self.toast_message = page.locator("//div[contains(@id,'toast-container')]")
        self.reset_password_link = page.locator("//a[contains(@class, 'footer-icon') and contains(@class, 'txt-primary')]")
        self.new_password_input = page.locator(
            '//label[normalize-space(text())="New Password"]/following-sibling::input[@type="password"]'
        )
        self.btn_update = page.locator(
            "//button[@type='button' and contains(@class, 'button-primary') and normalize-space()='Update']")

    # ---------------- Random helpers ----------------
    @staticmethod
    def random_string(length=6):
        return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

    @staticmethod
    def random_email():
        return f"{Admin_Add_User.random_string(6)}@yopmail.com"

    @staticmethod
    def random_login_id():
        return f"user_{Admin_Add_User.random_string(5)}"

    @staticmethod
    def random_employee_number():
        return str(random.randint(1000, 9999))

    # ---------------- Actions ----------------
    def navigate_to_admin(self):
        print("➡ Navigating to Admin page")
        self.helper.click(self.side_nav_admin, "Admin side navigation link")

    def click_add_user(self):
        self.helper.click(self.btn_add_user, "Add User button in the Admin page")

    def enter_name(self, name=None):
        if not name:
            name = f"User_{self.random_string(5)}"
        self.helper.enter_text(self.txt_name, name, "Name textbox")
        return name

    def enter_department(self, dept):
        self.helper.enter_text(self.txt_department, dept, "Department textbox")

    def enter_email(self, email=None):
        if not email:
            email = self.random_email()

        # ✅ Validate email format
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            print(f"❌ Invalid email format: '{email}'")
            pytest.fail(f"Invalid Email Format: {email}", pytrace=False)

        self.helper.enter_text(self.txt_email, email, "Email textbox")

    def enter_login_id(self, login_id=None):
        if not login_id:
            login_id = self.random_login_id()

        print(f"🔑 Entering Login ID: {login_id}")
        self.helper.enter_text(self.txt_login_id, login_id, "Login ID textbox")
        print(f"✅ Login ID entered successfully: {login_id}")
        return login_id

    def enter_employee_number(self, emp_no=None):
        if not emp_no:
            emp_no = self.random_employee_number()
        self.helper.enter_text(self.txt_employee_number, emp_no, "Employee Number textbox")

    def select_role(self, roles):
        if isinstance(roles, str):
            roles = [roles]

        print(f"🎯 Selecting roles: {roles}")
        self.helper.click(self.dropdown_role, "Roles dropdown")
        self.page.wait_for_timeout(1000)

        for role in roles:
            print(f"➡ Selecting role: '{role}'")
            role_option = self.page.get_by_text(role, exact=True)
            try:
                if role_option.count() > 0:
                    self.helper.click(role_option, f"Role option: {role}")
                    print(f"✅ Selected role: '{role}'")
                else:
                    print(f"⚠️ Role '{role}' not found.")
            except Exception as e:
                print(f"❌ Error selecting role '{role}': {e}")
            self.page.wait_for_timeout(500)

    def enter_whatsapp_number(self, country_code="91", whatsapp_no="9876543210"):
        self.helper.enter_text(self.country_code_input, country_code, "Country code input")
        self.helper.enter_text(self.whatsapp_input, whatsapp_no, "WhatsApp number input")

    def enable_send_welcome_mail(self):
        container = self.page.locator(
            '//div[@class="item" and .//label[contains(text(),"Send welcome mail to the user?")]]'
        )
        checkbox = container.locator('input[formcontrolname="sendMail"]')
        slider = container.locator('span.slider')

        container.wait_for(state="visible", timeout=5000)
        self.helper.scroll_to_label(container, "'Send welcome mail to the user?' toggle")

        is_checked = checkbox.evaluate("el => el.checked")
        if not is_checked:
            slider.click(force=True)
            self.page.wait_for_timeout(300)

        is_checked = checkbox.evaluate("el => el.checked")
        if is_checked:
            print("✔ 'Send welcome mail to the user?' toggle enabled")
        else:
            print("❌ Failed to enable 'Send welcome mail to the user?' toggle")

    def disable_user_status_toggle(self):
        # Locate the container div based on the label text
        container = self.page.locator(
            '//div[@class="item" and .//label[contains(text(),"Status")]]'
        )
        checkbox = container.locator('input[formcontrolname="status"]')
        slider = container.locator('span.slider')

        # Wait for container to be visible
        container.wait_for(state="visible", timeout=5000)
        self.helper.scroll_to_label(container, "'Status' toggle")

        # Check if the toggle is currently checked
        is_checked = checkbox.evaluate("el => el.checked")

        # If it is checked (enabled), click the slider to disable
        if is_checked:
            slider.click(force=True)
            self.page.wait_for_timeout(300)

        # Verify the toggle is now disabled
        is_checked = checkbox.evaluate("el => el.checked")
        if not is_checked:
            print("✔ 'Status' toggle disabled")
        else:
            print("❌ Failed to disable 'Status' toggle")

    def click_reset_password(self):
        """
        Clicks the reset password icon/link in the Admin page.
        """
        self.helper.click(
            self.reset_password_link,
            "Reset Password icon/link"
        )

    def click_save(self):
        """
        Clicks the Save button and validates if a toast appears.
        Stops test execution immediately if duplicate login ID or Employee No found.
        """
        self.helper.click(self.btn_save, "Save button")

        # Toast locator: supports both div/span structures
        toast_locator = self.page.locator("#toast-container div, #toast-container span")

        try:
            # Wait for toast to appear (max 5 seconds)
            toast_locator.first.wait_for(state="visible", timeout=5000)
            message = toast_locator.first.inner_text().strip()

            # Normalize whitespace to avoid gaps in logs
            message_clean = " ".join(message.split())
            print(f"⚠️ Toast message detected after Save: {message_clean}")

            # --- Duplicate validations ---
            if re.search(r"username\s*already\s*exists?", message_clean, re.IGNORECASE):
                error_msg = f"❌ Duplicate Login ID detected — {message_clean}"
                print(error_msg)
                pytest.fail(f"Duplicate Login ID: {message_clean}", pytrace=False)

            elif re.search(r"employee\s*no\s*already\s*exists?", message_clean, re.IGNORECASE):
                error_msg = f"❌ Duplicate Employee No detected — {message_clean}"
                print(error_msg)
                pytest.fail(f"Duplicate Employee No: {message_clean}", pytrace=False)

            # --- Generic error message handling ---
            elif re.search(r"(error|invalid|failed)", message_clean, re.IGNORECASE):
                error_msg = f"❌ Error message detected — {message_clean}"
                print(error_msg)
                pytest.fail(f"Form submission failed: {message_clean}", pytrace=False)

            else:
                print(f"✅ Success message: {message_clean}")

        except PlaywrightTimeoutError:
            # No toast appeared within timeout — assume success
            print("✅ No toast message detected — Save action successful.")
        except Exception as e:  # noqa: E722
            print(f"⚠️ Unexpected error while handling toast message: {e}")

    def click_all_users_radio(self):
        """Clicks the 'All Users' radio button."""
        self.radio_btn_all_users.click(force=True)

    def click_active_users_radio(self):
        """Clicks the 'Active Users' radio button."""
        self.radio_btn_active_users.click(force=True)

    def click_update(self):
        """
        Clicks the 'Update' button in the Reset Password dialog or section.
        """
        print("🖱️ Clicking the 'Update' button...")
        try:
            self.btn_update.wait_for(state="visible", timeout=5000)
            self.helper.click(self.btn_update, "Update button")
            print("✅ Clicked the 'Update' button successfully.")
        except Exception as e:
            self.helper.take_screenshot("ClickUpdateFailed")
            error_msg = f"❌ Failed to click 'Update' button: {e}"
            print(error_msg)
            raise AssertionError(error_msg)

    # ---------------------------------------------------------------
    # User Verification
    # ---------------------------------------------------------------
    def verify_user_in_all_users(self, username: str, description: str = "'All Users list'", timeout: int = 10000):
        """Verify that a specific user appears in the 'All Users' list."""
        print(f"\n🔍  Verifying if user '{username}' is listed under {description}...")
        try:
            user_locator = self.page.locator(
                f'//div[contains(@class,"admin-grid-item")]//p[normalize-space(text())="{username}"]'
            )
            user_locator.wait_for(state="visible", timeout=timeout)
            print(f"✅ 🏆  User '{username}' is visible in {description}.")
        except Exception as e:
            self.helper.take_screenshot(f"UserNotFound_{username}")
            error_msg = f"❌ Test failed — User '{username}' not found in {description}: {e}"
            print(error_msg)
            raise AssertionError(error_msg)

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

    def verify_user_in_active_list(self, username: str, timeout: int = 10000):
        """
        Switches to Active Users tab and verifies that the user appears there.
        """
        print(f"👁️  Checking if '{username}' appears in Active Users list...")
        self.click_active_users_radio()
        self.page.wait_for_timeout(2000)

        user_locator = self.page.locator(f'//p[normalize-space()="{username}"]')
        try:
            user_locator.wait_for(state="visible", timeout=timeout)
            print(f"✅ User '{username}' is displayed in Active Users list.")
            return True
        except:
            self.helper.take_screenshot(f"UserNotFoundInActive_{username}")
            raise AssertionError(f"❌ User '{username}' not found in Active Users list.")


    def verify_duplicate_login_toast(self, expected_message: str):
        """
        Click Save and check if expected duplicate toast appears.
        Takes screenshot if toast does not appear or message mismatch.
        """

        self.helper.click(self.btn_save, "Save button")

        toast_locator = self.page.locator("#toast-container div, #toast-container span")
        try:
            toast_locator.first.wait_for(state="visible", timeout=5000)
            message = toast_locator.first.inner_text().strip()
            print(f"⚠️ Toast message detected: {message}")

            if expected_message.lower() not in message.lower():
                # Take screenshot if message is not as expected
                self.helper.take_screenshot(prefix="DuplicateToastMismatch")
                pytest.fail(f"Expected message '{expected_message}', but got: '{message}'")

            print("✅ Negative test passed: Toast message displayed correctly")
            return True

        except PlaywrightTimeoutError:
            # Take screenshot if toast did not appear
            self.helper.take_screenshot(prefix="ToastNotFound")
            pytest.fail(f"❌ Expected toast message '{expected_message}' did not appear")

    def verify_duplicate_emp_toast(self):
        """
        Click Save and verify 'Employee No Already Exist' toast appears.
        Takes screenshot if toast does not appear or message mismatch.
        """
        self.helper.click(self.btn_save, "Save button")

        toast_locator = self.page.locator("#toast-container div, #toast-container span")
        try:
            toast_locator.first.wait_for(state="visible", timeout=5000)
            message = toast_locator.first.inner_text().strip()
            print(f"⚠️ Toast message detected: {message}")

            if "Employee No Already Exist" not in message:
                self.helper.take_screenshot(prefix="DuplicateEmpToastMismatch")
                pytest.fail(f"Expected duplicate employee number message, but got: '{message}'")

            print("✅ Negative test passed: Duplicate Employee Number message displayed correctly")

        except PlaywrightTimeoutError:
            self.helper.take_screenshot(prefix="DuplicateEmpToastNotFound")
            pytest.fail("❌ Expected duplicate Employee Number toast did not appear")

    def search_user(self, username: str, timeout: int = 5000):
        """
        Searches for a user in the user grid.
        """
        print(f"🔍 Searching for user '{username}'...")
        search_box = self.page.locator("#search-user-grid-records")
        search_box.wait_for(state="visible", timeout=timeout)
        search_box.fill("")  # clear old value
        search_box.fill(username)  # type username
        self.page.keyboard.press("Enter")  # trigger search
        self.page.wait_for_timeout(1500)  # wait for list refresh
        print(f"✅ User '{username}' search completed.")

    def click_user_in_all_users(self, username: str, description: str = "'All Users list'", timeout: int = 10000):
        """
        Clicks on a specific user in the 'All Users' list.
        """
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

    def enter_new_password(self, password: str, timeout: int = 5000):
        """
        Fills the 'New Password' field in the reset password form.
        """
        try:
            password_input = self.page.locator(
                '//label[normalize-space(text())="New Password"]/following-sibling::input[@type="password"]'
            )
            password_input.wait_for(state="visible", timeout=timeout)
            password_input.fill(password)
            print(f"✅ Entered new password in the reset form.")
        except Exception as e:
            self.helper.take_screenshot("EnterNewPasswordFailed")
            error_msg = f"❌ Failed to enter new password: {e}"
            print(error_msg)
            raise AssertionError(error_msg)

    # ---------------- Password Helpers ----------------
    def get_visible_password_rules(self) -> list[str]:
        """
        Type a temporary character to trigger validation container and
        return all currently visible password rules.
        """
        field = self.txt_password
        field.fill("a")  # Trigger password validation container
        self.page.wait_for_timeout(200)  # wait for DOM update

        rules_locator: Locator = self.page.locator("cf-password-policy-validate .password-validation ul li")
        visible_rules: list[str] = []

        count = rules_locator.count()
        for i in range(count):
            rule = rules_locator.nth(i)
            if rule.is_visible():
                visible_rules.append(rule.inner_text().strip())

        field.fill("")  # Optional: clear temporary character

        if visible_rules:
            print("🔍 Visible password validations:")
            for idx, rule in enumerate(visible_rules, start=1):
                print(f"{idx}. {rule}")
        else:
            print("✅ No visible password validations.")

        return visible_rules

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

    @staticmethod
    def add_char_for_rule(rules: list[str]) -> str:
        """
        Returns a single character that satisfies one of the unmet rules.
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
        # fallback
        return random.choice(string.ascii_letters + string.digits + "!@#$%^&*")

    def _rule_satisfied(self, rule: str, password: str) -> bool:
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
        return True  # fallback

    def generate_valid_password(self) -> str:
        """
        Generate a valid password based on the currently visible rules.
        Prints rules and the generated password.
        """
        password = ""
        field = self.txt_password
        visible_rules = self.get_visible_password_rules()
        min_len, max_len = self.parse_length_limits(visible_rules)

        # Keep adding characters to satisfy unmet rules
        while True:
            unmet_rules = [rule for rule in visible_rules if not self._rule_satisfied(rule, password)]
            if not unmet_rules:
                break
            if len(password) >= max_len:
                break
            password += self.add_char_for_rule(unmet_rules)
            field.fill(password)
            time.sleep(0.1)

        # Ensure minimum length
        while len(password) < min_len:
            password += random.choice(string.ascii_letters + string.digits + "!@#$%^&*")
            field.fill(password)
            time.sleep(0.05)

        print(f"🔑 Generated valid password: {password}")
        return password

    def enter_password(self, password: str | None = None) -> str:
        """
        Enters the password. If not provided, dynamically generates a valid one
        based on visible validation rules. Returns the final password for reuse.
        """
        if not password:
            password = self.generate_valid_password()
            # Fill it into the field as well
            self.helper.enter_text(self.txt_password, password, "Password textbox")
        else:
            self.helper.enter_text(self.txt_password, password, "Password textbox")

        return password

    def enter_new_password(self, password: str):
        """
        Enters a new password into the 'New Password' field
        in the Reset Password popup or section.
        """
        try:
            # Locator for the 'New Password' field
            new_password_field = self.page.locator(
                "//input[@type='password' and @name='reset=password-user']"
            )

            new_password_field.wait_for(state="visible", timeout=5000)
            self.helper.enter_text(new_password_field, password, "Reset Password field")
        except Exception as e:
            self.helper.take_screenshot("EnterNewPasswordFailed")
            error_msg = f"❌ Failed to enter new password: {e}"
            print(error_msg)
            raise AssertionError(error_msg)

    def reset_password_with_policy_check(self, old_password: str | None = None) -> str:
        """
        Resets user password with policy validation:
          1️⃣ Click reset password link
          2️⃣ Try old password (expected to fail with policy toast)
          3️⃣ Generate and enter a new valid password
          4️⃣ Click Update and verify success

        Returns the new valid password.
        """
        print("\n🔁 Starting Reset Password Validation Flow...\n")

        # --- Step 0️⃣: Resolve old password ---
        if not old_password:
            if hasattr(self, "current_password") and self.current_password:
                old_password = self.current_password
                print(f"ℹ️ Using stored old password: {old_password}")
            else:
                raise ValueError("❌ No old password available. Pass one or set self.current_password before calling.")

        # --- Step 1️⃣: Click 'Reset Password' link ---
        self.click_reset_password()

        # --- Step 2️⃣: Enter same old password (expected to fail) ---
        print(f"🧪 Attempting to reset using old password: {old_password}")
        self.enter_new_password(old_password)
        self.helper.click(self.btn_update, "Update button (old password attempt)")

        # --- Step 3️⃣: Expect 'not met password policy' toast ---
        toast_locator = self.page.locator("#toast-container div, #toast-container span")
        try:
            toast_locator.first.wait_for(state="visible", timeout=5000)
            message = toast_locator.first.inner_text().strip()
            print(f"⚠️ Toast message detected: {message}")

            if "not met" in message.lower() or "policy" in message.lower():
                print("✅ Policy validation triggered correctly — old password rejected.")
            else:
                self.helper.take_screenshot("UnexpectedToast_ResetPassword")
                pytest.fail(f"❌ Unexpected toast message: '{message}'", pytrace=False)

        except PlaywrightTimeoutError:
            self.helper.take_screenshot("NoToast_ResetPassword")
            pytest.fail("❌ No toast message appeared after entering old password.", pytrace=False)

        # --- Step 4️⃣: Generate new valid password ---
        print("\n🔑 Generating a new valid password according to policy...")
        new_password = self.generate_valid_password()
        print(f"🧩 Retrying with valid password: {new_password}")

        self.enter_new_password(new_password)

        # Wait for policy validation to pass (no invalid rules visible)
        try:
            self.page.locator("//li[contains(@class, 'invalid_Password')]").wait_for(state="hidden", timeout=5000)
            print("✅ Password validation rules cleared — proceeding to update.")
        except PlaywrightTimeoutError:
            print("⚠️ Some password rules still visible, continuing with update anyway.")

        # --- Step 5️⃣: Click Update and verify result ---
        self.helper.click(self.btn_update, "Update button (valid password)")
        self.page.wait_for_timeout(2000)  # short wait to allow toast to appear

        try:
            toast_locator.first.wait_for(state="visible", timeout=5000)
            message = toast_locator.first.inner_text().strip()
            print(f"📩 Toast after valid password: {message}")

            success_patterns = [
                "password updated successfully",
                "password has been updated",
                "password changed successfully",
            ]
            failure_patterns = [
                "password not met",
                "invalid password",
                "failed",
                "error",
            ]

            if any(p in message.lower() for p in success_patterns):
                print("✅ Password updated successfully.")
            elif any(p in message.lower() for p in failure_patterns):
                self.helper.take_screenshot("PasswordUpdateFailed")
                pytest.fail(f"❌ Password update failed — '{message}'", pytrace=False)
            else:
                self.helper.take_screenshot("UnexpectedToastMessage")
                pytest.fail(f"⚠️ Unexpected toast message: '{message}'", pytrace=False)

        except PlaywrightTimeoutError:
            if self.btn_update.is_visible():
                self.helper.take_screenshot("UpdateStillVisible_AfterValidPassword")
                pytest.fail("❌ Update button still visible — password update likely failed.", pytrace=False)
            else:
                print("✅ No toast appeared but Update button hidden — assuming success.")

        # --- Step 6️⃣: Store new password for reuse ---
        self.current_password = new_password
        print(f"🔁 Password reset successful. Stored new password: {new_password}")

        return new_password

    # ---------------------------------------------------------------
    # 🔒 Invalid Password Generation & Negative Testing
    # ---------------------------------------------------------------
    def generate_invalid_passwords(self) -> list[tuple[str, str]]:
        """
        Dynamically generates invalid passwords for each visible validation rule.
        Returns a list of tuples (rule_text, invalid_password).
        """
        field = self.txt_password

        # Trigger the container by typing a character
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
        min_len, max_len = Admin_Add_User.parse_length_limits(visible_rules)

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
                invalid_pwd = ''.join(random.choices(string.ascii_letters + string.digits, k=target_len))

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
            self.page.wait_for_timeout(1500)

            # Click Save
            self.helper.click(self.btn_save, "Save button")
            self.page.wait_for_timeout(2000)

            try:
                if self.btn_save.is_visible():
                    print(f"✅ Negative case passed — Save button still visible for rule: '{rule}'")
                else:
                    screenshot_name = f"InvalidPassword_{re.sub(r'[^0-9a-zA-Z]+', '_', rule)[:30]}"
                    self.helper.take_screenshot(screenshot_name)
                    pytest.fail(f"❌ Invalid password accepted for rule '{rule}'. Screenshot: {screenshot_name}",
                                pytrace=False)

            except Exception as _:
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
