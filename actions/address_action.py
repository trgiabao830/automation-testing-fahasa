import allure
from playwright.sync_api import Page

from pages.address_page import AddressLocators


class AddressActions:
    def __init__(self, page: Page):
        self.page = page
        self.locators = AddressLocators(page)

    @allure.step("Truy cập trang Quản lý Sổ địa chỉ")
    def navigate_to_address_book(self):
        """Action: Truy cập vào trang Quản lý Sổ địa chỉ"""
        self.page.goto("https://www.fahasa.com/customer/address/")

    @allure.step("Bấm nút Thêm địa chỉ mới")
    def click_add_new_address(self):
        """Action: Bấm nút Thêm địa chỉ mới"""
        self.locators.add_address_button.first.click()

    @allure.step("Bấm nút Sửa tại thẻ Địa chỉ thanh toán mặc định")
    def click_edit_billing_address(self):
        """Action: Bấm nút 'Sửa' ở thẻ Địa chỉ thanh toán mặc định"""
        self.locators.billing_card.locator("a", has_text="Sửa").click()

    @allure.step("Bấm nút Sửa tại thẻ Địa chỉ giao hàng mặc định")
    def click_edit_shipping_address(self):
        """Action: Bấm nút 'Sửa' ở thẻ Địa chỉ giao hàng mặc định"""
        self.locators.shipping_card.locator("a", has_text="Sửa").click()

    @allure.step("Điền thông tin liên hệ - Họ: '{lastname}', Tên: '{firstname}', SĐT: '{phone}'")
    def fill_contact_info(self, lastname: str, firstname: str, phone: str):
        """Action: Điền thông tin liên hệ"""
        self.locators.lastname_input.fill(lastname)
        self.locators.firstname_input.fill(firstname)
        self.locators.phone_input.fill(phone)

    @allure.step("Chọn vị trí địa lý")
    def select_location(
        self,
        country: str = None,
        region: str = None,
        city: str = None,
        ward: str = None,
    ):
        """Action: Chọn vị trí địa lý từ dropdown"""
        if country:
            self.locators.country_select.select_option(label=country)
        if region:
            self.locators.region_select.select_option(label=region)
        if city:
            self.locators.city_select.select_option(label=city)
        if ward:
            self.locators.ward_select.select_option(label=ward)

    @allure.step("Điền số nhà/đường: '{street}' và zipcode: '{zipcode}'")
    def fill_street_and_zip(self, street: str, zipcode: str):
        """Action: Điền số nhà và mã bưu điện"""
        self.locators.street_input.fill(street)
        self.locators.zipcode_input.fill(zipcode)

    @allure.step("Đánh dấu làm địa chỉ thanh toán mặc định")
    def set_as_default_billing(self):
        """Action: Đánh dấu đây là địa chỉ thanh toán mặc định"""
        self.locators.primary_billing_checkbox.check(force=True)

    @allure.step("Đánh dấu làm địa chỉ giao hàng mặc định")
    def set_as_default_shipping(self):
        """Action: Đánh dấu đây là địa chỉ giao hàng mặc định"""
        self.locators.primary_shipping_checkbox.check(force=True)
    
    @allure.step("Bấm nút Lưu địa chỉ")    
    def submit_address(self):
        """Action: Bấm nút Lưu"""
        self.locators.save_button.click()

    @allure.step("Đọc thông báo lỗi Native HTML5 của trình duyệt trên ô Số điện thoại")
    def get_phone_native_validation_message(self) -> str:
        """Đọc thông báo báo lỗi HTML5 mặc định của trình duyệt trên ô số điện thoại"""
        return self.locators.phone_input.evaluate("node => node.validationMessage")

    @allure.step("Đọc dữ liệu từ thẻ hiển thị địa chỉ ({card_type}) trên UI")
    def get_address_card_details(self, card_type="billing"):
        """Đọc họ tên, số điện thoại, đường và khu vực từ thẻ địa chỉ"""
        card = (
            self.locators.billing_card
            if card_type == "billing"
            else self.locators.shipping_card
        )

        fullname = card.locator(".address-book-fullname").inner_text().strip()
        phone = card.locator(".address-book-title span").nth(1).inner_text().strip()
        street = card.locator(".text-address-value").nth(0).inner_text().strip()
        location = card.locator(".text-address-value").nth(1).inner_text().strip()

        return {
            "fullname": fullname,
            "phone": phone,
            "street": street,
            "location": location,
        }