import allure
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


class LoginActions:
    def __init__(self, page: Page):
        self.page = page
        self.locators = LoginLocators(page)

    @allure.step("Truy cập trang chủ và mở form đăng nhập")
    def navigate_to_login(self):
        self.page.goto("https://www.fahasa.com/")
        self.locators.account_link.click()

    @allure.step("Thực hiện đăng nhập với Username: '{username}' và Submit bằng: '{submit_by}'")
    def login(self, username: str = "", password: str = "", submit_by: str = "enter"):
        """
        Action: Đăng nhập vào hệ thống.
        - Nếu username/password = "" (rỗng), hệ thống sẽ mô phỏng việc focus vào ô rồi bỏ qua.
        - submit_by = "enter" hoặc "click".
        """
        if username:
            self.locators.username_input.fill(username)
        else:
            self.locators.username_input.click()

        if password:
            self.locators.password_input.click()
            self.locators.password_input.press_sequentially(password, delay=10)
        else:
            if not username: 
                pass
            else:
                self.locators.password_input.click()

        if submit_by.lower() == "click":
            self.locators.password_input.press("Tab") 
            self.locators.login_button.click()
        else:
            self.page.keyboard.press("Enter")