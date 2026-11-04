import json
import allure
import pytest
from pathlib import Path
from playwright.sync_api import Page, expect
from pages.changepassword_page import ChangePasswordActions


def load_changepassword_data():
    data_path = Path(__file__).parent.parent / "data" / "changepassword_data.json"
    with open(data_path, "r", encoding="utf-8") as file:
        return json.load(file)


TEST_DATA = load_changepassword_data()


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
    changepassword_actions.change_password("", "", "")

    expect(changepassword_actions.locators.current_password_error).to_have_text(
        TEST_DATA["expected_messages"]["empty_field"]
    )
    expect(changepassword_actions.locators.new_password_error).to_have_text(
        TEST_DATA["expected_messages"]["empty_field"]
    )
    expect(changepassword_actions.locators.confirm_password_error).to_have_text(
        TEST_DATA["expected_messages"]["empty_field"]
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
    cur = (
        "" if omit_field == "current" else TEST_DATA["valid_inputs"]["current_password"]
    )
    new = "" if omit_field == "new" else TEST_DATA["valid_inputs"]["new_password"]
    conf = (
        "" if omit_field == "confirm" else TEST_DATA["valid_inputs"]["confirm_password"]
    )

    changepassword_actions.change_password(cur, new, conf)

    # Assert động bằng getattr
    error_locator = getattr(changepassword_actions.locators, error_locator_name)
    expect(error_locator).to_have_text(TEST_DATA["expected_messages"]["empty_field"])


# TC3: Sai mật khẩu hiện tại
@allure.epic("Account Management")
@allure.feature("Change Password")
@allure.story("Form Validation")
@allure.title("Đổi mật khẩu thất bại do sai mật khẩu hiện tại")
def test_wrong_current_password(changepassword_actions: ChangePasswordActions):
    wrong_current = TEST_DATA["invalid_inputs"]["wrong_current"]

    changepassword_actions.change_password(
        wrong_current,
        TEST_DATA["valid_inputs"]["new_password"],
        TEST_DATA["valid_inputs"]["confirm_password"],
    )

    expect(changepassword_actions.locators.error_message).to_have_text(
        TEST_DATA["expected_messages"]["wrong_current_pass"]
    )


# TC4: Mật khẩu xác nhận không khớp
@allure.epic("Account Management")
@allure.feature("Change Password")
@allure.story("Form Validation")
@allure.title("Đổi mật khẩu thất bại do mật khẩu xác nhận không khớp")
def test_mismatch_confirm_password(changepassword_actions: ChangePasswordActions):
    mismatch_conf = TEST_DATA["invalid_inputs"]["mismatch_confirm"]

    changepassword_actions.change_password(
        TEST_DATA["valid_inputs"]["current_password"],
        TEST_DATA["valid_inputs"]["new_password"],
        mismatch_conf,
    )

    expect(changepassword_actions.locators.confirm_password_error).to_have_text(
        TEST_DATA["expected_messages"]["mismatch_pass"]
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
    invalid_pass = TEST_DATA["invalid_inputs"][invalid_key]

    # Nhập mật khẩu mới sai quy định, ô confirm nhập y hệt để pass qua lỗi "mismatch"
    changepassword_actions.change_password(
        TEST_DATA["valid_inputs"]["current_password"], invalid_pass, invalid_pass
    )

    expect(changepassword_actions.locators.new_password_error).to_have_text(
        TEST_DATA["expected_messages"][expected_msg_key]
    )


# TC7: Đổi mật khẩu thành công
@allure.epic("Account Management")
@allure.feature("Change Password")
@allure.story("Update Password Luồng Chính")
@allure.title("Đổi mật khẩu thành công và tự động Revert")
@allure.severity(allure.severity_level.CRITICAL)
def test_change_password_success(changepassword_actions: ChangePasswordActions):
    changepassword_actions.change_password(
        TEST_DATA["valid_inputs"]["current_password"],
        TEST_DATA["valid_inputs"]["new_password"],
        TEST_DATA["valid_inputs"]["confirm_password"],
    )

    expect(changepassword_actions.locators.success_message).to_have_text(
        TEST_DATA["expected_messages"]["update_success"]
    )

    # Nếu không đổi lại, các test case chạy sau sẽ bị đăng nhập thất bại
    with allure.step(
        "Revert: Đổi lại mật khẩu cũ để không làm hỏng state.json cho các test case sau"
    ):
        changepassword_actions.navigate_to_change_password()
        changepassword_actions.change_password(
            TEST_DATA["valid_inputs"]["new_password"],
            TEST_DATA["valid_inputs"]["current_password"],
            TEST_DATA["valid_inputs"]["current_password"],
        )
