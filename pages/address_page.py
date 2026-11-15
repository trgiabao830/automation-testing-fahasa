from playwright.sync_api import Page

class AddressLocators:
    def __init__(self, page: Page):
        self.page = page

        self.add_address_button = page.get_by_text("Thêm địa chỉ mới").first
        self.save_button = page.locator("button[title='Lưu địa chỉ']").first

        self.lastname_input = page.locator("#lastname")
        self.firstname_input = page.locator("#firstname")
        self.phone_input = page.locator("#telephone")
        self.street_input = page.locator("#street_1")
        self.zipcode_input = page.locator("#zip")

        self.country_select = page.locator("#country")
        self.region_select = page.locator("#region_id")  # Tỉnh/Thành
        self.city_select = page.locator("#city_id")  # Quận/Huyện
        self.ward_select = page.locator("#ward_id")  # Phường/Xã

        self.primary_billing_checkbox = page.locator("#primary_billing")
        self.primary_shipping_checkbox = page.locator("#primary_shipping")

        self.success_message = page.locator(".messages .success-msg span").first

        self.billing_card = page.locator(".address-book-container").filter(
            has_text="Địa chỉ thanh toán mặc định"
        )
        self.shipping_card = page.locator(".address-book-container").filter(
            has_text="Địa chỉ giao hàng mặc định"
        )

        def get_error_for(locator):
            return (
                self.page.locator(".edit-input-container")
                .filter(has=locator)
                .locator(".validation-advice")
                .first
            )

        self.lastname_error = get_error_for(self.lastname_input)
        self.firstname_error = get_error_for(self.firstname_input)
        self.phone_error = get_error_for(self.phone_input)
        self.street_error = get_error_for(self.street_input)
        self.zipcode_error = get_error_for(self.zipcode_input)

        self.country_error = get_error_for(self.country_select)
        self.region_error = get_error_for(self.region_select)
        self.city_error = get_error_for(self.city_select)
        self.ward_error = get_error_for(self.ward_select)