import allure
from playwright.sync_api import Page

from pages.login_page import LoginLocators


class LoginActions:
    def __init__(self, page: Page):
        self.page = page
        self.locators = LoginLocators(page)

    @allure.step("Truy cập trang chủ và mở form đăng nhập")
    def navigate_to_login(self):
        self.page.goto("https://www.fahasa.com/")
        self.locators.account_link.click()

    @allure.step("Nhập username: {username}")
    def fill_username(self, username: str):
        self.locators.username_input.fill(username)

    @allure.step("Click vào ô username rỗng")
    def click_empty_username(self):
        self.locators.username_input.click()
    
    @allure.step("Nhập password: {password}")    
    def fill_password(self, password: str):
        self.locators.password_input.click()
        self.locators.password_input.press_sequentially(password, delay=10)
    
    @allure.step("Click vào ô password rỗng")
    def click_empty_password(self):
        self.locators.password_input.click()
        
    @allure.step("Click vào nút đăng nhập")
    def click_login_button(self):
        self.locators.login_button.click()
        
    @allure.step("Nhấn Enter để submit")
    def press_enter(self):
        self.page.keyboard.press("Enter")
            