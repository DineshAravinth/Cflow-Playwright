import pytest
from PageObjects.Login_Page.A_loginpage import LoginPage
from PageObjects.Admin_Add_User.B_Admin_Add_user import (
    AdminNavigationAndAddUser,
    UserVerificationAndDuplicateEmpNOLoginChecks,
    PasswordGenerationAndValidation,
    NewUserLoginVerification
)
from Utilities.BaseHelpers import BaseHelper
from Utilities.ReadProperties import ReadConfig

# Use the top-level playwright instance
from conftest import playwright  # global sync_playwright().start() instance


def test_verify_new_user_login_standalone():
    # -------------------------- MAIN BROWSER → Create User --------------------------
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(viewport={"width": 1470, "height": 720})
    page = context.new_page()

    region = "Test"
    url = ReadConfig.getURL(region)
    client_id = ReadConfig.getClientID(region)
    admin_user = ReadConfig.getUsername(region)
    admin_pass = ReadConfig.getPassword(region)

    page.goto(url)

    lp = LoginPage(page)
    lp.setClientid(client_id)
    lp.setUserName(admin_user)
    lp.setPassword(admin_pass)
    lp.clickLogin()

    helper = BaseHelper(page)
    helper.verify_page_url("/dashboard", "Dashboard")

    admin_nav = AdminNavigationAndAddUser(page, helper)
    user_verif = UserVerificationAndDuplicateEmpNOLoginChecks(page, helper, admin_nav)
    password_util = PasswordGenerationAndValidation(page, helper)

    admin_nav.go_to_admin()
    page.wait_for_timeout(800)

    admin_nav.click_add_user()
    username = admin_nav.enter_name()
    login_id = admin_nav.enter_login_id()
    password = password_util.enter_password()
    admin_nav.enter_department("QA")
    admin_nav.enter_email("autotest@yopmail.com")
    admin_nav.enter_employee_number()
    admin_nav.select_role(["User"])
    admin_nav.enter_whatsapp_number("91", "9988776655")
    admin_nav.enable_send_welcome_mail()
    admin_nav.click_save()
    page.wait_for_timeout(1500)

    admin_nav.click_All_Users_radio()
    page.wait_for_timeout(800)
    admin_nav.search_user(username, timeout=1000)
    user_verif.verify_user_in_all_users(username)
    user_verif.verify_user_status_toggle(username)

    context.close()
    browser.close()
    print("🧹 Main browser closed after user creation.")

    # -------------------------- SECOND BROWSER → Verify Login --------------------------
    # Launch a fresh browser & context for isolated login
    browser2 = playwright.chromium.launch(headless=False)
    context2 = browser2.new_context(viewport={"width": 1470, "height": 720})
    page2 = context2.new_page()

    login_verifier = NewUserLoginVerification(
        page=page2,  # pass the page, NOT the browser
        login_url="https://testapp.cflowapps.com/cflow/login"
    )

    login_verifier.verify_new_user_login(
        client_id="cflowautomation.com",
        login_id=login_id,
        password=password,
        username=username
    )

    context2.close()
    browser2.close()
    print("🧹 Second browser closed after login verification.")

    print("🛑 Playwright test completed without triggering asyncio loop errors.")
