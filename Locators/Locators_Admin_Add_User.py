from playwright.sync_api import Page

class Admin_Add_User_Locators:
    def __init__(self, page: Page):

        # 🔹 Buttons
        # Opens the 'Add User' form from the Admin page
        self.btn_add_user = page.get_by_role("button", name="Add User")

        # 🔹 Text Fields
        # Input field for entering the user's full name
        self.txt_name = page.locator('input[formcontrolname="name"]')

        # Input field for entering the user's department name
        self.txt_department = page.locator('input[formcontrolname="department"]')

        # Input field for entering the user's email address
        self.txt_email = page.locator('input[formcontrolname="email"]')

        # Input field for setting a unique login ID for the user
        self.txt_login_id = page.locator('input[formcontrolname="loginId"]')

        # Input field for setting the user's password
        self.txt_password = page.locator('input[formcontrolname="password"]')

        # Input field for the employee number / staff ID
        self.txt_employee_number = page.locator('input[formcontrolname="empNo"]')

        # 🔹 Dropdowns
        # Role selection dropdown to assign access level to the user
        self.dropdown_role = page.locator('ng-select[formcontrolname="role"]')

        # To verify the selected role
        self.verify_role =page.locator("//ng-select[@formcontrolname='role']//span[contains(@class,'ng-value-label')]")

        # 🔹 Toggle / Checkbox
        # Send Welcome Mail Toggle
        self.send_welcome_mail_container = page.locator(
            '//div[@class="item" and .//label[contains(text(),"Send welcome mail to the user?")]]'
        )
        self.send_welcome_mail_checkbox = self.send_welcome_mail_container.locator('input[formcontrolname="sendMail"]')
        self.send_welcome_mail_slider = self.send_welcome_mail_container.locator('span.slider')
        self.toggle_send_mail = self.send_welcome_mail_container.locator('label.switch')

        # User Status Toggle
        self.user_status_container = page.locator(
            '//div[@class="item" and .//label[contains(text(),"Status")]]'
        )
        self.user_status_checkbox = self.user_status_container.locator('input[formcontrolname="status"]')
        self.user_status_slider = self.user_status_container.locator('span.slider')

        # 🔹 Action Buttons
        # Button to save or submit the Add User form
        self.btn_save = page.locator('//button[normalize-space(text())="Save"]')

        # 🔹 Phone Number Fields
        # Country code input field (e.g., +91)
        self.country_code_input = page.locator('//div[contains(@class, "d-flex")]/input[@placeholder="+91"]')

        # WhatsApp number input field for the user
        self.whatsapp_input = page.locator('//div[contains(@class, "d-flex")]/input[@formcontrolname="whatsappNo"]')

        # 🔹 Radio Buttons "active users" / "all users" pages
        # Radio button for filtering or selecting "All Users"
        self.radio_btn_all_users = page.locator('//label[.//span[normalize-space()="All Users"]]')

        # Radio button for filtering or selecting only "Active Users"
        self.radio_btn_active_users = page.locator('//label[.//span[normalize-space()="Active Users"]]')

        # 🔹 Notifications
        # Toast message container used for success/error notifications
        self.toast_message = page.locator("//div[contains(@id,'toast-container')]")

        # 🔹 Reset Password Section
        # Link/button to initiate the password reset process
        self.reset_password_link = page.locator(
            "//a[contains(@class, 'footer-icon') and contains(@class, 'txt-primary')]"
        )

        # Input field for entering a new password when resetting
        self.new_password_input = page.locator(
            '//label[normalize-space(text())="New Password"]/following-sibling::input[@type="password"]'
        )

        # Button to confirm and update the new password
        self.btn_update = page.locator(
            "//button[@type='button' and contains(@class, 'button-primary') and normalize-space()='Update']"
        )

        # 🔹 Search
        # Search bar for filtering users in the user list/grid
        self.search_box = page.locator("#search-user-grid-records")

        # To Import the user
        self.btn_import = page.locator('//button[.//span[normalize-space()="Import"]]')

        # To upload a file
        self.input_upload_file = page.locator('//input[@type="file" and @id="file"]')

        # To click the upload button
        self.btn_upload = page.locator('//button[normalize-space()="Upload"]')

        #Lookup page locators
        # Click the employees lookup
        self.click_employees_lookup = page.locator("//a[.//p[normalize-space(text())='Employees']]")




