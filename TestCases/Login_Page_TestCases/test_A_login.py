from PageObjects.Login_Page.A_loginpage import LoginPage

class Test_001_Login:
    def test_homepage(self, login):
        page = login
        lp = LoginPage(page)
