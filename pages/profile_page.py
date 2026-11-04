import allure
from playwright.sync_api import Page

class ProfileLocators:
    def __init__(self, page: Page):
        self.lastname_input = page.locator("#lastname")
        self.firstname_input = page.locator("#firstname")
        self.save_button = page.locator(".btn-save-confirm")
        
        self.lastname_error = (
            page.locator(".fhs-input-box")
            .filter(has=self.lastname_input)
            .locator(".fhs-input-alert")
        )
        
        self.firstname_error = (
            page.locator(".fhs-input-box")
            .filter(has=self.firstname_input)
            .locator(".fhs-input-alert")
        )

        self.success_message = page.locator(".messages .success-msg span").first
        self.error_message = page.locator(".messages .error-msg span").first

class ProfileActions:
    def __init__(self, page: Page):
        self.page = page
        self.locators = ProfileLocators(page)

    @allure.step("Truy cập trang Thông tin tài khoản - Hồ sơ cá nhân")
    def navigate_to_profile(self):
        self.page.goto("https://www.fahasa.com/customer/account/edit/")

    @allure.step("Cập nhật Profile - Họ: '{lastname}', Tên: '{firstname}'")
    def update_profile(self, lastname: str, firstname: str):
        """Action: Xóa text cũ, Cập nhật thông tin Lastname và Firstname"""
        self.locators.lastname_input.fill(lastname)
        self.locators.firstname_input.fill(firstname)
        self.locators.save_button.click()