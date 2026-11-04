import json
import allure
import pytest
from pathlib import Path
from playwright.sync_api import Page, expect
from pages.profile_page import ProfileActions


def load_profile_data():
    data_path = Path(__file__).parent.parent / "data" / "profile_data.json"
    with open(data_path, "r", encoding="utf-8") as file:
        return json.load(file)


TEST_DATA = load_profile_data()


@pytest.fixture
def profile_actions(auth_page: Page):
    actions = ProfileActions(auth_page)
    actions.navigate_to_profile()
    return actions


@allure.epic("Account Management")
@allure.feature("Profile")
@allure.story("Form Validation")
@pytest.mark.parametrize(
    "lastname_val, firstname_val, locator_name",
    [
        ("", TEST_DATA["valid_inputs"]["firstname"], "lastname_error"),  # TC1: Trống Họ
        (
            TEST_DATA["valid_inputs"]["lastname"],
            "",
            "firstname_error",
        ),  # TC2: Trống Tên
    ],
    ids=["Empty_Lastname", "Empty_Firstname"],
)
def test_empty_fields(
    profile_actions: ProfileActions, lastname_val, firstname_val, locator_name
):
    field_name = "Họ" if locator_name == "lastname_error" else "Tên"
    allure.dynamic.title(f"Cập nhật thất bại do để trống trường: {field_name}")

    # Action
    profile_actions.update_profile(lastname_val, firstname_val)

    # Assert
    expected_msg = TEST_DATA["expected_messages"]["empty_field"]

    error_locator = getattr(profile_actions.locators, locator_name)
    expect(error_locator).to_have_text(expected_msg)


@allure.epic("Account Management")
@allure.feature("Profile")
@allure.story("Form Validation")
@pytest.mark.parametrize(
    "input_key",
    [
        "numbers_only",  # TC3: Họ tên là số
        "special_chars_only",  # TC4: Ký tự đặc biệt
        "mixed_chars",  # TC5: Chữ + Ký tự đặc biệt
        "over_64_chars",  # TC6: Hơn 64 ký tự
    ],
    ids=["Numbers_Only", "Special_Chars_Only", "Mixed_Chars", "Over_64_Chars"],
)
def test_invalid_characters_format(profile_actions: ProfileActions, input_key):
    allure.dynamic.title(f"Cập nhật thất bại do sai định dạng Họ Tên - {input_key}")

    invalid_str = TEST_DATA["invalid_inputs"][input_key]

    # Action
    profile_actions.update_profile(invalid_str, invalid_str)

    # Assert
    expected_msg = TEST_DATA["expected_messages"]["invalid_characters"]
    expect(profile_actions.locators.error_message).to_have_text(expected_msg)


# TC7: Cập nhật thành công
@allure.epic("Account Management")
@allure.feature("Profile")
@allure.story("Update Profile Luồng Chính")
@allure.title("Cập nhật thông tin Profile thành công")
@allure.severity(allure.severity_level.CRITICAL)
def test_update_profile_success(profile_actions: ProfileActions):
    valid_last = TEST_DATA["valid_inputs"]["lastname"]
    valid_first = TEST_DATA["valid_inputs"]["firstname"]

    profile_actions.update_profile(valid_last, valid_first)

    expected_msg = TEST_DATA["expected_messages"]["update_success"]
    expect(profile_actions.locators.success_message).to_have_text(expected_msg)
