from PageObjects.Admin_Add_User.B_Admin_Add_user import (
    AdminNavigationAndAddUser,
    UserVerificationAndDuplicateEmpNOLoginChecks,
    PasswordGenerationAndValidation,
    InvalidPasswordTests
)
from Utilities.BaseHelpers import BaseHelper
from Locators.Locators_Admin_Add_User import Admin_Add_User_Locators



class Test_002_Admin_Add_User_Negative_cases:

    def test_TC01_add_user_with_duplicate_login_id(self, login):
        """
        🚨 Negative Test: Verify 'Username Already Exist' toast for duplicate Login ID
        """
        page = login
        helper = BaseHelper(page)
        admin_nav = AdminNavigationAndAddUser(page, helper)
        user_verif = UserVerificationAndDuplicateEmpNOLoginChecks(page, helper, admin_nav)
        password_util = PasswordGenerationAndValidation(page, helper)

        print("🚨 Starting Negative Test: Duplicate Login ID")

        # Navigate to Admin
        admin_nav.go_to_admin()
        page.wait_for_timeout(1000)

        # Add User
        admin_nav.click_add_user()
        page.wait_for_timeout(2000)

        # Fill mandatory fields with duplicate login
        admin_nav.enter_name("Existing_User")
        admin_nav.enter_department("QA")
        admin_nav.enter_email("existinguser@yopmail.com")

        duplicate_login_id = "dinesh01"  # 🔁 Known duplicate
        admin_nav.enter_login_id(duplicate_login_id)
        password_util.enter_password()
        admin_nav.enter_employee_number("123466")
        admin_nav.select_role(["User"])
        admin_nav.enter_whatsapp_number(country_code="91", whatsapp_no="9988776655")

        # Verify duplicate login toast
        user_verif.verify_duplicate_login_toast("Username Already Exist")


    def test_TC02_add_user_with_duplicate_emp_no(self, login):
        """
        🚨 Negative Test: Verify 'Employee No Already Exist' toast for duplicate Employee No
        """
        page = login
        helper = BaseHelper(page)
        admin_nav = AdminNavigationAndAddUser(page, helper)
        user_verif = UserVerificationAndDuplicateEmpNOLoginChecks(page, helper, admin_nav)
        password_util = PasswordGenerationAndValidation(page, helper)

        print("🚨 Starting Negative Test: Duplicate Employee Number")
        page.reload()

        # Navigate to Admin
        admin_nav.go_to_admin()
        page.wait_for_timeout(1000)

        # Add User
        admin_nav.click_add_user()
        page.wait_for_timeout(2000)

        # Fill mandatory fields with duplicate Employee No
        admin_nav.enter_name("Existing_Employee")
        admin_nav.enter_department("QA")
        admin_nav.enter_email("existingemp@yopmail.com")
        admin_nav.enter_login_id("unique_login_id_00552")
        password_util.enter_password()

        duplicate_emp_no = "E02"  # 🔁 Known duplicate
        admin_nav.enter_employee_number(duplicate_emp_no)
        admin_nav.select_role(["User"])
        admin_nav.enter_whatsapp_number(country_code="91", whatsapp_no="9988776655")

        # Verify duplicate Employee toast
        user_verif.verify_duplicate_emp_toast()

    def test_TC03_add_user_with_invalid_passwords(self, login):
        """
        🚨 Negative Test: Dynamically test invalid passwords for each password rule.
        Save button must remain visible (form not submitted) for all invalid passwords.
        """
        page = login
        helper = BaseHelper(page)
        admin_nav = AdminNavigationAndAddUser(page, helper)
        locators = Admin_Add_User_Locators(page)

        # Initialize InvalidPasswordTests with required locators
        password_util = InvalidPasswordTests(
            page,
            helper,
            txt_password_locator=locators.txt_password,
            btn_save_locator=locators.btn_save
        )

        print("🚨 Starting Negative Test: Invalid Password Validations")
        page.reload()
        page.wait_for_timeout(1000)

        # Navigate to Admin page
        admin_nav.go_to_admin()
        page.wait_for_timeout(1000)

        # Open Add User form
        admin_nav.click_add_user()
        page.wait_for_timeout(2000)

        # Fill mandatory fields (password will be tested dynamically)
        admin_nav.enter_name("Invalid_Password_User")
        admin_nav.enter_department("QA")
        admin_nav.enter_email()
        admin_nav.enter_login_id()
        admin_nav.enter_employee_number()
        admin_nav.select_role(["User"])
        admin_nav.enter_whatsapp_number(country_code="91", whatsapp_no="9876543210")

        # Run dynamic invalid password tests
        password_util.test_invalid_passwords()

        print("✅ Completed all invalid password validation tests successfully.")
