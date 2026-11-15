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