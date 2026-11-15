import allure
from playwright.sync_api import Page

from pages.profile_page import ProfileLocators


class ProfileActions:
    def __init__(self, page: Page):
        self.page = page
        self.locators = ProfileLocators(page)

    @allure.step("Truy cập trang Thông tin tài khoản - Hồ sơ cá nhân")
    def navigate_to_profile(self):
        self.page.goto("https://www.fahasa.com/customer/account/edit/")

    @allure.step("Nhập Họ: '{lastname}'")
    def fill_lastname(self, lastname: str):
        self.locators.lastname_input.fill(lastname)

    @allure.step("Nhập Tên: '{firstname}'")
    def fill_firstname(self, firstname: str):
        self.locators.firstname_input.fill(firstname)

    @allure.step("Nhấn nút Lưu thay đổi")
    def click_save_button(self):
        self.locators.save_button.click()
