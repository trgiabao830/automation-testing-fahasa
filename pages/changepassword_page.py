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