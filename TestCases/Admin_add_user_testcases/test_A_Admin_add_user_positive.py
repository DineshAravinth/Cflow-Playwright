import pytest
from playwright.sync_api import sync_playwright, Browser, Page
from PageObjects.Admin_Add_User.B_Admin_Add_user import (
    AdminNavigationAndAddUser,
    UserVerificationAndDuplicateEmpNOLoginChecks,
    PasswordGenerationAndValidation,
    VerifyUserInEmployeesLookup,
    ImportUserFromExcel,
    NewUserLoginVerification
)
from Utilities.BaseHelpers import BaseHelper
from Utilities.ReadProperties import ReadConfig




class Test_01AdminAddUserPositiveCases:
    """✅ Admin Add User Positive Test Suite"""
    created_username = None       # for first user (active)
    created_password = None
    created_emp_no = None
    created_login_id = None
    disabled_username = None      # for second user (disabled)

    def test_TC01_add_user_with_active_status(self, login):
        page = login
        helper = BaseHelper(page)
        admin_nav = AdminNavigationAndAddUser(page, helper)
        user_verif = UserVerificationAndDuplicateEmpNOLoginChecks(page, helper, admin_nav)
        password_util = PasswordGenerationAndValidation(page, helper)

        print("\n🚀 Starting Test: Add User with Active Status")

        # Navigate to Admin
        admin_nav.go_to_admin()
        page.wait_for_timeout(1000)
        helper.verify_page_url("/user-role-permission", "Admin")

        # Add user
        admin_nav.click_add_user()
        page.wait_for_timeout(1000)

        username = admin_nav.enter_name()
        admin_nav.enter_department("QA")
        admin_nav.enter_email("dinesh123@yopmail.com")

        # Capture the randomly generated Login ID
        login_id = admin_nav.enter_login_id()

        old_password = password_util.enter_password()
        emp_no = admin_nav.enter_employee_number()
        admin_nav.select_role(["User", "Admin"])
        admin_nav.enter_whatsapp_number(country_code="91", whatsapp_no="9988776655")
        admin_nav.enable_send_welcome_mail()
        page.wait_for_timeout(500)

        # Save
        admin_nav.click_save()
        page.wait_for_timeout(2000)
        print(f"✅ User '{username}' added successfully with Active status")

        # Store user details for next test
        Test_01AdminAddUserPositiveCases.created_username = username
        Test_01AdminAddUserPositiveCases.created_password = old_password
        Test_01AdminAddUserPositiveCases.created_emp_no = emp_no
        Test_01AdminAddUserPositiveCases.created_login_id = login_id   # 👈 store login ID

        # Verify in All Users
        admin_nav.click_All_Users_radio()
        page.wait_for_timeout(1500)
        admin_nav.search_user(username, timeout=1000)
        user_verif.verify_user_in_all_users(username)
        user_verif.verify_user_status_toggle(username)


    def test_TC02_verify_user_in_employee_lookup(self, login):

        page = login
        helper = BaseHelper(page)
        emp_lookup_verif = VerifyUserInEmployeesLookup(page, helper)

        username = Test_01AdminAddUserPositiveCases.created_username
        emp_no = Test_01AdminAddUserPositiveCases.created_emp_no
        login_id = Test_01AdminAddUserPositiveCases.created_login_id  # 👈 fetch stored login ID

        if not username or not emp_no or not login_id:
            pytest.skip("⚠ No created user details from previous test — skipping lookup verification.")

        expected_data = {
            "Employee No": emp_no,
            "Employee Name": username,
            "Login ID": login_id,       # 👈 updated
            "Email ID": "dinesh123@yopmail.com",
            "Department": "QA"
        }

        print(f"\n🔍 Verifying Employee Lookup entry for user: {username}")

        # Step 1️⃣ - Navigate to Lookup section
        emp_lookup_verif.go_to_lookup()
        page.wait_for_timeout(1000)

        # Step 2️⃣ - Click Employees Lookup tab
        emp_lookup_verif.employees_lookup()
        page.wait_for_timeout(2000)

        # Step 3️⃣ - Verify the latest employee record
        emp_lookup_verif.verify_latest_employee_record(expected_data)

    def test_TC03_reset_password_of_created_user(self, login):

        page = login
        helper = BaseHelper(page)
        admin_nav = AdminNavigationAndAddUser(page, helper)
        password_util = PasswordGenerationAndValidation(page, helper)

        username = Test_01AdminAddUserPositiveCases.created_username
        old_password = Test_01AdminAddUserPositiveCases.created_password
        if not username or not old_password:
            pytest.skip("⚠ No user found from previous test — skipping password reset.")

        print("\n🚀 Resetting password for created user")

        admin_nav.go_to_admin()
        page.wait_for_timeout(1000)
        admin_nav.click_All_Users_radio()
        admin_nav.search_user(username, timeout=2000)
        admin_nav.click_user_in_All_Users_page(username)
        page.wait_for_timeout(2000)

        password_util.reset_password_with_policy_check(old_password)

    def test_TC04_add_user_with_disabled_status(self, login):
        page = login
        helper = BaseHelper(page)
        admin_nav = AdminNavigationAndAddUser(page, helper)
        user_verif = UserVerificationAndDuplicateEmpNOLoginChecks(page, helper, admin_nav)
        password_util = PasswordGenerationAndValidation(page, helper)

        print("\n🚀 Starting Test: Add User with Disabled Status")
        # page.reload()
        page.wait_for_timeout(1000)

        # Navigate and add user
        admin_nav.go_to_admin()
        helper.verify_page_url("/user-role-permission", "Admin")
        admin_nav.click_add_user()
        page.wait_for_timeout(2000)

        username = admin_nav.enter_name()
        admin_nav.enter_department("QA")
        admin_nav.enter_email("dinesh123@yopmail.com")
        admin_nav.enter_login_id()
        password_util.enter_password()
        admin_nav.enter_employee_number()
        admin_nav.select_role(["User"])
        admin_nav.enter_whatsapp_number(country_code="91", whatsapp_no="9988776655")

        # Disable status and enable welcome mail
        admin_nav.disable_user_status_toggle()
        admin_nav.enable_send_welcome_mail()

        # Save
        admin_nav.click_save()
        page.wait_for_timeout(2000)
        print(f"✅ User '{username}' added successfully with Disabled status")

        # Verify
        admin_nav.click_All_Users_radio()
        admin_nav.search_user(username, timeout=2000)
        user_verif.verify_user_in_all_users(username)
        user_verif.verify_user_status_toggle_disabled(username)

        print(f"\n🚀 Enabling user '{username}' and verifying in Active Users")
        user_verif.enable_user_toggle(username)
        print(f"✅ Enabled user '{username}' successfully")

        # Verify in Active Users
        admin_nav.click_Active_Users_radio_()
        admin_nav.search_user(username, timeout=2000)
        user_verif.verify_user_in_Active_List(username)
        print(f"🎯 Verified '{username}' now appears in Active Users page\n")

        # Store for next test
        Test_01AdminAddUserPositiveCases.disabled_username = username

    def test_TC05_verify_imported_users(self,login):

        # --- Test Data ---
        file_path = "TestData/User_Import.xlsx"

        page = login
        helper = BaseHelper(page)
        admin_nav = AdminNavigationAndAddUser(page, helper)
        import_user_verify = ImportUserFromExcel(page, helper)

        # --- Step 1️⃣: Navigate to Admin page ---
        admin_nav.go_to_admin()
        page.wait_for_timeout(2000)

        # --- Step 2️⃣: Start Import ---
        import_user_verify.click_import()
        page.wait_for_timeout(2000)

        # --- Step 3️⃣: Upload Excel file ---
        import_user_verify.upload_file(file_path)
        page.wait_for_timeout(2000)

        # --- Step 4️⃣: Click Upload and handle toast/popup ---
        import_user_verify.click_upload()
        page.wait_for_timeout(5000)

        # --- Step 5️⃣: Verify imported users data from Excel ---
        import_user_verify.verify_imported_users_from_excel(file_path)

    def test_TC06_verify_new_user_login_standalone(self, browser, page, login):
        """🧪 Create a user → Close session → Verify login in fresh browser"""
        page = login
        helper = BaseHelper(page)
        admin_nav = AdminNavigationAndAddUser(page, helper)
        user_verif = UserVerificationAndDuplicateEmpNOLoginChecks(page, helper, admin_nav)
        password_util = PasswordGenerationAndValidation(page, helper)

        print("\n🚀 Starting Test: Standalone New User Login Verification")

        # --------------- STEP 1: Create New User (using logged-in page) ---------------
        admin_nav.go_to_admin()
        admin_nav.click_add_user()

        username = admin_nav.enter_name()
        login_id = admin_nav.enter_login_id()
        password = password_util.enter_password()
        admin_nav.enter_department("QA")
        admin_nav.enter_email("autotest@yopmail.com")
        admin_nav.enter_employee_number()
        admin_nav.select_role(["User"])
        admin_nav.enable_send_welcome_mail()
        admin_nav.click_save()
        page.wait_for_timeout(2000)

        # Verify user created
        admin_nav.click_All_Users_radio()
        admin_nav.search_user(username, timeout=2000)
        user_verif.verify_user_in_all_users(username)

        print(f"🎯 User created successfully: {username} | {login_id}")

        # --------------- STEP 2: Open Fresh Browser to Verify Login ---------------
        context2 = browser.new_context(viewport={"width": 1470, "height": 720})
        page2 = context2.new_page()

        login_verifier = NewUserLoginVerification(
            page=page2,
            login_url=ReadConfig.getURL("Test")
        )

        login_verifier.verify_new_user_login(
            client_id=ReadConfig.getClientID("Test"),
            login_id=login_id,
            password=password,
            username=username
        )

        context2.close()
        print("✨ New user login verified successfully in standalone browser!")
