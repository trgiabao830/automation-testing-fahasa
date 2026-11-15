import json
import allure
import pytest
from pathlib import Path
from playwright.sync_api import Page, expect
from actions.profile_action import ProfileActions


def load_profile_data():
    data_path = Path(__file__).parent.parent / "data" / "profile_data.json"
    with open(data_path, "r", encoding="utf-8") as file:
        return json.load(file)


TEST_DATA = load_profile_data()
VALID_INPUTS = TEST_DATA["valid_inputs"]
INVALID_INPUTS = TEST_DATA["invalid_inputs"]
EXPECTED_MESSAGES = TEST_DATA["expected_messages"]


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
        ("", VALID_INPUTS["firstname"], "lastname_error"),  # TC1: Trống Họ
        (
            VALID_INPUTS["lastname"],
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
    profile_actions.fill_lastname(lastname_val)
    profile_actions.fill_firstname(firstname_val)
    profile_actions.click_save_button()

    # Assert
    error_locator = getattr(profile_actions.locators, locator_name)
    expect(error_locator).to_have_text(EXPECTED_MESSAGES["empty_field"])


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

    # Action
    profile_actions.fill_lastname(INVALID_INPUTS[input_key])
    profile_actions.fill_firstname(INVALID_INPUTS[input_key])
    profile_actions.click_save_button()

    # Assert
    expect(profile_actions.locators.error_message).to_have_text(
        EXPECTED_MESSAGES["invalid_characters"]
    )


# TC7: Cập nhật thành công
@allure.epic("Account Management")
@allure.feature("Profile")
@allure.story("Update Profile Luồng Chính")
@allure.title("Cập nhật thông tin Profile thành công")
@allure.severity(allure.severity_level.CRITICAL)
def test_update_profile_success(profile_actions: ProfileActions):

    # Action
    profile_actions.fill_lastname(VALID_INPUTS["lastname"])
    profile_actions.fill_firstname(VALID_INPUTS["firstname"])
    profile_actions.click_save_button()

    # Assert
    expect(profile_actions.locators.success_message).to_have_text(
        EXPECTED_MESSAGES["update_success"]
    )
