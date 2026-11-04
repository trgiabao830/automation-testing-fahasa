import allure
from playwright.sync_api import Page

class ChangePasswordLocators:
    def __init__(self, page: Page):
        self.page = page
        
        self.current_password_input = page.locator("#current_password")
        self.new_password_input = page.locator("#password")
        self.confirm_password_input = page.locator("#confirmation")
        
        self.save_button = page.locator("#btn-confirm-change-password")
        
        self.current_password_error = (
            page.locator(".fhs-input-box")
            .filter(has=self.current_password_input)
            .locator(".fhs-input-alert")
        )
        
        self.new_password_error = (
            page.locator(".fhs-input-box")
            .filter(has=self.new_password_input)
            .locator(".fhs-input-alert")
        )
        
        self.confirm_password_error = (
            page.locator(".fhs-input-box")
            .filter(has=self.confirm_password_input)
            .locator(".fhs-input-alert")
        )
        
        self.success_message = page.locator(".messages .success-msg span").first
        self.error_message = page.locator(".messages .error-msg span").first
        
class ChangePasswordActions:
    def __init__(self, page: Page):
        self.page = page
        self.locators = ChangePasswordLocators(page)

    @allure.step("Truy cập trang Đổi mật khẩu")
    def navigate_to_change_password(self):
        self.page.goto("https://www.fahasa.com/customer/changepassword/")

    @allure.step("Thực hiện Đổi mật khẩu (Cũ: '{current_password}', Mới: '{new_password}', Xác nhận: '{confirm_password}')")
    def change_password(self, current_password: str, new_password: str, confirm_password: str):
        """Action: Điền thông tin mật khẩu và bấm nút Lưu"""
        self.locators.current_password_input.fill(current_password)
        self.locators.new_password_input.fill(new_password)
        self.locators.confirm_password_input.fill(confirm_password)
        self.locators.save_button.click()