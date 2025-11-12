import pytest
from PageObjects.B_Admin_Add_user import Admin_Add_User
from Utilities.BaseHelpers import BaseHelper


class Test_001_Admin_Add_User_Positive_Cases:
    """
    ✅ Test Suite: Admin Add User (Positive Scenarios)
    Covers:
        1️⃣ Add user with Active status
        2️⃣ Add user with Disabled status
        3️⃣ Enable that Disabled user and verify under Active Users
    """

    # class-level variable to share username between tests
    disabled_username = None

    def test_add_user_with_active_status(self, login):
        page = login
        admin = Admin_Add_User(page)
        helper = BaseHelper(page)

        print("\n🚀  Starting Test Case: 'Add User in Admin Module with Active Status'")

        # Step 1: Navigate to Admin section
        admin.navigate_to_admin()
        page.wait_for_timeout(1000)
        helper.verify_page_url("/user-role-permission", "Admin")

        # Step 2: Click Add User
        admin.click_add_user()
        page.wait_for_timeout(2000)

        # Step 3: Fill user details
        username = admin.enter_name()
        page.wait_for_timeout(500)
        admin.enter_department("QA")
        admin.enter_email("dinesh123@yopmail.com")
        admin.enter_login_id()
        old_password = admin.enter_password()
        admin.enter_employee_number()
        admin.select_role(["User"])
        admin.enter_whatsapp_number(country_code="91", whatsapp_no="9988776655")
        admin.enable_send_welcome_mail()
        page.wait_for_timeout(500)

        # Step 4: Save User
        admin.click_save()
        page.wait_for_timeout(2000)
        print(f"✅ User '{username}' added successfully with Active status")

        # Step 5: Verify user under All Users
        admin.click_all_users_radio()
        admin.verify_user_in_all_users(username)
        status = admin.verify_user_status_toggle(username)
        print(f"🎯 Verified '{username}' appears under All Users with status: {status}")

        print("\n✅ Test Completed: 'Add User with Active Status'\n")

        # Step 6️⃣: Open user and reset password
        admin.search_user(username)
        admin.click_user_in_all_users(username)
        page.wait_for_timeout(2000)
        admin.reset_password_with_policy_check(old_password)



    def test_add_user_with_disabled_status(self, login):
        page = login
        admin = Admin_Add_User(page)
        helper = BaseHelper(page)

        print("\n🚀  Starting Test Case: 'Add User in Admin Module with Disabled Status'")

        page.reload()
        page.wait_for_timeout(1000)

        # Step 1: Navigate to Admin section
        admin.navigate_to_admin()
        helper.verify_page_url("/user-role-permission", "Admin")

        # Step 2: Click Add User
        admin.click_add_user()
        page.wait_for_timeout(2000)

        # Step 3: Fill user details
        username = admin.enter_name()
        admin.enter_department("QA")
        admin.enter_email("dinesh123@yopmail.com")
        admin.enter_login_id()
        admin.enter_password()
        admin.enter_employee_number()
        admin.select_role(["User"])
        admin.enter_whatsapp_number(country_code="91", whatsapp_no="9988776655")

        # Disable status and enable welcome mail
        admin.disable_user_status_toggle()
        admin.enable_send_welcome_mail()

        # Step 4: Save user
        admin.click_save()
        page.wait_for_timeout(2000)

        print(f"\n✅ User '{username}' added successfully with Disabled status")

        # Step 5: Verify under All Users
        admin.click_all_users_radio()
        admin.verify_user_in_all_users(username)
        status = admin.verify_user_status_toggle_disabled(username)
        print(f"🎯 Verified '{username}' appears under All Users with status: {status}")

        # Store username for next test
        Test_001_Admin_Add_User_Positive_Cases.disabled_username = username
        print(f"\n📦 Stored disabled username for next test: {username}")
        print("\n➡ Next: Enable this user and verify under Active Users.\n")

    # -------------------------------------------------------------------

    def test_enable_and_verify_active_user(self, login):
        page = login
        admin = Admin_Add_User(page)
        helper = BaseHelper(page)

        username = Test_001_Admin_Add_User_Positive_Cases.disabled_username

        if not username:
            pytest.skip("⚠ No disabled user found from previous test — skipping this scenario.")

        print(f"\n🚀 Starting Test: Enable user '{username}' and verify under Active Users")

        # Step 1: Verify toggle is currently disabled
        admin.verify_user_status_toggle_disabled(username)

        # Step 2: Enable toggle
        admin.enable_user_toggle(username)
        print(f"✅ Enabled user '{username}' successfully")

        # Step 3: Verify in Active Users list
        admin.click_active_users_radio()
        admin.verify_user_in_active_list(username)

        print(f"🎯 Verified '{username}' now appears under Active Users list.")
        print("\n✅ Test Completed: 'Enable and Verify Active User'\n")







