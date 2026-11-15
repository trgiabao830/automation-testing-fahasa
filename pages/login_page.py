from playwright.sync_api import Page


class LoginLocators:
    def __init__(self, page: Page):
        self.account_link = page.get_by_role("link", name="Tài khoản", exact=True)
        self.username_input = page.locator("#login_username")
        self.password_input = page.locator("#login_password")
        self.login_button = page.locator("button.fhs-btn-login")

        self.username_error = (
            page.locator(".fhs-input-box")
            .filter(has=self.username_input)
            .locator(".fhs-input-alert")
        )
        self.password_error = (
            page.locator(".fhs-input-box")
            .filter(has=self.password_input)
            .locator(".fhs-input-alert")
        )
        self.general_error = page.locator(".fhs-popup-msg.fhs-login-msg")
