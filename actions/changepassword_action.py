import allure
from playwright.sync_api import Page

from pages.changepassword_page import ChangePasswordLocators


class ChangePasswordActions:
    def __init__(self, page: Page):
        self.page = page
        self.locators = ChangePasswordLocators(page)

    @allure.step("Truy cập trang Đổi mật khẩu")
    def navigate_to_change_password(self):
        self.page.goto("https://www.fahasa.com/customer/changepassword/")

    @allure.step("Nhập mật khẩu hiện tại: '{current_password}'")
    def fill_current_password(self, current_password: str):
        self.locators.current_password_input.fill(current_password)
        
    @allure.step("Nhập mật khẩu mới: '{new_password}'")    
    def fill_new_password(self, new_password: str):
        self.locators.new_password_input.fill(new_password)
    
    @allure.step("Nhập xác nhận mật khẩu mới: '{confirm_password}'")
    def fill_confirm_password(self, confirm_password: str):
        self.locators.confirm_password_input.fill(confirm_password)
        
    @allure.step("Bấm nút Lưu thay đổi")
    def click_save_button(self):
        self.locators.save_button.click()
