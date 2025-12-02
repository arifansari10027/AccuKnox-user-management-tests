from playwright.sync_api import Page, expect


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username_input = page.get_by_placeholder("Username")
        self.password_input = page.get_by_placeholder("Password")
        self.login_button = page.get_by_role("button", name="Login")

    def goto(self):
        self.page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")

    def login_as_admin(self, username: str = "Admin", password: str = "admin123"):
        """
        Go to login page and log in using given credentials.
        """
        self.goto()
        expect(self.username_input).to_be_visible(timeout=10000)
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
        # Verify that Dashboard page is loaded
        expect(
            self.page.get_by_role("heading", name="Dashboard")
        ).to_be_visible(timeout=10000)
