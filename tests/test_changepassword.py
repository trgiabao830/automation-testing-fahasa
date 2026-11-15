import json
import allure
import pytest
from pathlib import Path
from playwright.sync_api import Page, expect
from actions.changepassword_action import ChangePasswordActions


def load_changepassword_data():
    data_path = Path(__file__).parent.parent / "data" / "changepassword_data.json"
    with open(data_path, "r", encoding="utf-8") as file:
        return json.load(file)


TEST_DATA = load_changepassword_data()
VALID_INPUTS = TEST_DATA["valid_inputs"]
INVALID_INPUTS = TEST_DATA["invalid_inputs"]
EXPECTED_MESSAGES = TEST_DATA["expected_messages"]


@pytest.fixture
def changepassword_actions(auth_page: Page):
    actions = ChangePasswordActions(auth_page)
    actions.navigate_to_change_password()
    return actions


# TC1: Để trống tất cả các field
@allure.epic("Account Management")
@allure.feature("Change Password")
@allure.story("Form Validation")
@allure.title("Đổi mật khẩu thất bại do để trống tất cả thông tin")
def test_empty_all_fields(changepassword_actions: ChangePasswordActions):
    
    # Action
    changepassword_actions.fill_current_password("")
    changepassword_actions.fill_new_password("")
    changepassword_actions.fill_confirm_password("")
    changepassword_actions.click_save_button()

    # Assert
    expect(changepassword_actions.locators.current_password_error).to_have_text(
        EXPECTED_MESSAGES["empty_field"]
    )
    expect(changepassword_actions.locators.new_password_error).to_have_text(
        EXPECTED_MESSAGES["empty_field"]
    )
    expect(changepassword_actions.locators.confirm_password_error).to_have_text(
        EXPECTED_MESSAGES["empty_field"]
    )


# TC2: Để trống từng field
@allure.epic("Account Management")
@allure.feature("Change Password")
@allure.story("Form Validation")
@pytest.mark.parametrize(
    "omit_field, error_locator_name",
    [
        ("current", "current_password_error"),
        ("new", "new_password_error"),
        ("confirm", "confirm_password_error"),
    ],
    ids=["Omit_Current", "Omit_New", "Omit_Confirm"],
)
def test_empty_single_field(
    changepassword_actions: ChangePasswordActions, omit_field, error_locator_name
):
    allure.dynamic.title(f"Đổi mật khẩu thất bại do bỏ trống trường: {omit_field}")
    # Setup data: Nếu là field bị omit thì gán rỗng, ngược lại lấy data hợp lệ
    cur = "" if omit_field == "current" else VALID_INPUTS["current_password"]
    new = "" if omit_field == "new" else VALID_INPUTS["new_password"]
    conf = "" if omit_field == "confirm" else VALID_INPUTS["confirm_password"]

    # Action
    changepassword_actions.fill_current_password(cur)
    changepassword_actions.fill_new_password(new)
    changepassword_actions.fill_confirm_password(conf)
    changepassword_actions.click_save_button()

    # Assert động bằng getattr
    error_locator = getattr(changepassword_actions.locators, error_locator_name)
    expect(error_locator).to_have_text(EXPECTED_MESSAGES["empty_field"])


# TC3: Sai mật khẩu hiện tại
@allure.epic("Account Management")
@allure.feature("Change Password")
@allure.story("Form Validation")
@allure.title("Đổi mật khẩu thất bại do sai mật khẩu hiện tại")
def test_wrong_current_password(changepassword_actions: ChangePasswordActions):
    
    # Action
    changepassword_actions.fill_current_password(INVALID_INPUTS["wrong_current"])
    changepassword_actions.fill_new_password(VALID_INPUTS["new_password"])
    changepassword_actions.fill_confirm_password(VALID_INPUTS["confirm_password"])
    changepassword_actions.click_save_button()

    # Assert
    expect(changepassword_actions.locators.error_message).to_have_text(
        EXPECTED_MESSAGES["wrong_current_pass"]
    )


# TC4: Mật khẩu xác nhận không khớp
@allure.epic("Account Management")
@allure.feature("Change Password")
@allure.story("Form Validation")
@allure.title("Đổi mật khẩu thất bại do mật khẩu xác nhận không khớp")
def test_mismatch_confirm_password(changepassword_actions: ChangePasswordActions):

    # Action
    changepassword_actions.fill_current_password(VALID_INPUTS["current_password"])
    changepassword_actions.fill_new_password(VALID_INPUTS["new_password"])
    changepassword_actions.fill_confirm_password(INVALID_INPUTS["mismatch_confirm"])
    changepassword_actions.click_save_button()

    # Assert
    expect(changepassword_actions.locators.confirm_password_error).to_have_text(
        EXPECTED_MESSAGES["mismatch_pass"]
    )


# TC5 & TC6: Độ dài mật khẩu không hợp lệ (dưới 6 ký tự hoặc trên 30 ký tự)
@allure.epic("Account Management")
@allure.feature("Change Password")
@allure.story("Form Validation")
@pytest.mark.parametrize(
    "invalid_key, expected_msg_key",
    [("short_password", "short_pass"), ("long_password", "long_pass")],
    ids=["Short_Password_Under_6", "Long_Password_Over_30"],
)
def test_password_length_validation(
    changepassword_actions: ChangePasswordActions, invalid_key, expected_msg_key
):
    allure.dynamic.title(
        f"Đổi mật khẩu thất bại do độ dài không hợp lệ - {invalid_key}"
    )

    # Action
    changepassword_actions.fill_current_password(VALID_INPUTS["current_password"])
    changepassword_actions.fill_new_password(INVALID_INPUTS[invalid_key])
    changepassword_actions.fill_confirm_password(INVALID_INPUTS[invalid_key])
    changepassword_actions.click_save_button()

    # Assert
    expect(changepassword_actions.locators.new_password_error).to_have_text(
        EXPECTED_MESSAGES[expected_msg_key]
    )


# TC7: Đổi mật khẩu thành công
@allure.epic("Account Management")
@allure.feature("Change Password")
@allure.story("Update Password Luồng Chính")
@allure.title("Đổi mật khẩu thành công và tự động Revert")
@allure.severity(allure.severity_level.CRITICAL)
def test_change_password_success(changepassword_actions: ChangePasswordActions):
    
    # Action
    changepassword_actions.fill_current_password(VALID_INPUTS["current_password"])
    changepassword_actions.fill_new_password(VALID_INPUTS["new_password"])
    changepassword_actions.fill_confirm_password(VALID_INPUTS["confirm_password"])
    changepassword_actions.click_save_button()

    # Assert
    expect(changepassword_actions.locators.success_message).to_have_text(
        EXPECTED_MESSAGES["update_success"]
    )

    # Nếu không đổi lại, các test case chạy sau sẽ bị đăng nhập thất bại
    with allure.step(
        "Revert: Đổi lại mật khẩu cũ để không làm hỏng state.json cho các test case sau"
    ):
        changepassword_actions.navigate_to_change_password()
        changepassword_actions.fill_current_password(VALID_INPUTS["new_password"])
        changepassword_actions.fill_new_password(VALID_INPUTS["current_password"])
        changepassword_actions.fill_confirm_password(VALID_INPUTS["current_password"])
        changepassword_actions.click_save_button()