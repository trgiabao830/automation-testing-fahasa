import json
import allure
import pytest
from pathlib import Path
from playwright.sync_api import Page, expect
from pages.address_page import AddressActions


def load_address_data():
    data_path = Path(__file__).parent.parent / "data" / "address_data.json"
    with open(data_path, "r", encoding="utf-8") as file:
        return json.load(file)


TEST_DATA = load_address_data()


@pytest.fixture
def address_actions(auth_page: Page):
    actions = AddressActions(auth_page)
    actions.navigate_to_address_book()
    return actions


@allure.epic("Account Management")
@allure.feature("Address Book")
@allure.story("Form Validation")
@pytest.mark.parametrize(
    "omit_field, error_locator_name, expected_msg_key",
    [
        ("lastname", "lastname_error", "empty_text"),  # TC1: Bỏ trống Họ
        ("phone", "phone_error", "empty_text"),  # TC2: Bỏ trống SĐT
        ("street", "street_error", "empty_text"),  # TC3: Bỏ trống Đường
        (
            "region",
            "region_error",
            "empty_select",
        ),  # TC4: Bỏ trống Tỉnh/Thành (không chọn Region)
    ],
    ids=["Omit_Lastname", "Omit_Phone", "Omit_Street", "Omit_Region"],
)
def test_empty_single_field(
    address_actions: AddressActions, omit_field, error_locator_name, expected_msg_key
):
    allure.dynamic.title(f"Thêm địa chỉ thất bại do bỏ trống trường: {omit_field}")

    address_actions.click_add_new_address()

    # Điền tất cả, trừ field bị loại trừ
    ln = "" if omit_field == "lastname" else TEST_DATA["valid_inputs"]["lastname"]
    fn = "" if omit_field == "firstname" else TEST_DATA["valid_inputs"]["firstname"]
    ph = "" if omit_field == "phone" else TEST_DATA["valid_inputs"]["phone"]
    st = "" if omit_field == "street" else TEST_DATA["valid_inputs"]["street"]

    address_actions.fill_contact_info(ln, fn, ph)
    address_actions.fill_street_and_zip(st, TEST_DATA["valid_inputs"]["zipcode"])

    # Xử lý Dropdown
    if omit_field != "region":
        address_actions.select_location(region=TEST_DATA["valid_inputs"]["region"])
        address_actions.page.wait_for_timeout(500)
        address_actions.select_location(
            city=TEST_DATA["valid_inputs"]["city"],
            ward=TEST_DATA["valid_inputs"]["ward"],
        )

    address_actions.submit_address()

    # Lấy đúng locator báo lỗi tương ứng để Assert
    error_locator = getattr(address_actions.locators, error_locator_name)
    expect(error_locator).to_have_text(TEST_DATA["expected_messages"][expected_msg_key])


@allure.epic("Account Management")
@allure.feature("Address Book")
@allure.story("Form Validation")
@pytest.mark.parametrize(
    "invalid_key, expected_msg_key",
    [
        ("letters_only", "phone_native_format"),  # TC5: SĐT là chữ
        ("special_chars", "phone_native_format"),  # TC6: SĐT là ký tự đặc biệt
        ("short_phone", "phone_native_short"),  # TC7: SĐT ít hơn 10 số
    ],
    ids=["Letters_Only", "Special_Chars", "Short_Phone"],
)
def test_invalid_phone_native_validation(
    address_actions: AddressActions, invalid_key, expected_msg_key
):
    allure.dynamic.title(
        f"Thêm địa chỉ thất bại do sai định dạng SĐT (Bắt JS) - {invalid_key}"
    )

    invalid_phone = TEST_DATA["invalid_inputs"]["phones"][invalid_key]

    address_actions.click_add_new_address()
    address_actions.fill_contact_info(
        TEST_DATA["valid_inputs"]["lastname"],
        TEST_DATA["valid_inputs"]["firstname"],
        invalid_phone,
    )
    address_actions.submit_address()

    # 1. Đọc thông báo native validation từ trình duyệt
    actual_validation_msg = address_actions.get_phone_native_validation_message()

    # 2. Lấy chuỗi mong đợi từ JSON
    expected_msg_prefix = TEST_DATA["expected_messages"][expected_msg_key]

    # 3. Kiểm chứng
    assert expected_msg_prefix in actual_validation_msg


@allure.epic("Account Management")
@allure.feature("Address Book")
@allure.story("Address Management Luồng Chính")
@pytest.mark.parametrize(
    "default_type",
    [
        "billing",  # TC8: Đặt địa chỉ vừa thêm làm mặc định thanh toán
        "shipping",  # TC9: Đặt địa chỉ vừa thêm làm mặc định giao hàng
    ],
    ids=["Set_Default_Billing", "Set_Default_Shipping"],
)
def test_change_default_address(address_actions: AddressActions, default_type):
    allure.dynamic.title(f"Thay đổi địa chỉ mặc định thành công - Dạng: {default_type}")

    new_default = TEST_DATA["new_default_address"]

    address_actions.click_add_new_address()

    address_actions.fill_contact_info(
        new_default["lastname"], new_default["firstname"], new_default["phone"]
    )
    address_actions.fill_street_and_zip(
        new_default["street"], TEST_DATA["valid_inputs"]["zipcode"]
    )
    address_actions.select_location(
        country=new_default["country"], region=new_default["region"]
    )
    address_actions.page.wait_for_timeout(500)  # Đợi API load Quận/Huyện
    address_actions.select_location(city=new_default["city"], ward=new_default["ward"])

    if default_type == "billing":
        address_actions.set_as_default_billing()
    else:
        address_actions.set_as_default_shipping()

    address_actions.submit_address()
    expect(address_actions.locators.success_message).to_have_text(
        TEST_DATA["expected_messages"]["update_success"]
    )

    actual_details = address_actions.get_address_card_details(card_type=default_type)
    expected_fullname = f"{new_default['lastname']} {new_default['firstname']}"

    assert actual_details["fullname"] == expected_fullname


# TC10: Thêm địa chỉ mới thành công
@allure.epic("Account Management")
@allure.feature("Address Book")
@allure.story("Address Management Luồng Chính")
@allure.title("Thêm mới địa chỉ thành công (Không set mặc định)")
@allure.severity(allure.severity_level.CRITICAL)
def test_add_new_address_success(address_actions: AddressActions):
    address_actions.click_add_new_address()

    address_actions.fill_contact_info(
        TEST_DATA["valid_inputs"]["lastname"],
        TEST_DATA["valid_inputs"]["firstname"],
        TEST_DATA["valid_inputs"]["phone"],
    )
    address_actions.fill_street_and_zip(
        TEST_DATA["valid_inputs"]["street"], TEST_DATA["valid_inputs"]["zipcode"]
    )

    address_actions.select_location(
        country=TEST_DATA["valid_inputs"]["country"],
        region=TEST_DATA["valid_inputs"]["region"],
    )
    address_actions.page.wait_for_timeout(300)  # Đợi API load Quận/Huyện
    address_actions.select_location(
        city=TEST_DATA["valid_inputs"]["city"], ward=TEST_DATA["valid_inputs"]["ward"]
    )

    address_actions.submit_address()

    expect(address_actions.locators.success_message).to_have_text(
        TEST_DATA["expected_messages"]["update_success"]
    )


# TC11: Sửa địa chỉ mặc định thành công
@allure.epic("Account Management")
@allure.feature("Address Book")
@allure.story("Address Management Luồng Chính")
@allure.title("Sửa địa chỉ thanh toán mặc định hiện có thành công")
def test_update_default_address(address_actions: AddressActions):
    new_street = TEST_DATA["edit_address"]["new_street"]

    address_actions.click_edit_billing_address()  # Click nút sửa
    address_actions.fill_street_and_zip(
        new_street, TEST_DATA["valid_inputs"]["zipcode"]
    )
    address_actions.submit_address()

    expect(address_actions.locators.success_message).to_have_text(
        TEST_DATA["expected_messages"]["update_success"]
    )

    # Kiểm tra UI thẻ địa chỉ có cập nhật đúng đường vừa sửa chưa
    actual_details = address_actions.get_address_card_details(card_type="billing")
    assert actual_details["street"] == new_street
