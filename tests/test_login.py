import json
import allure
import pytest
from pathlib import Path
from playwright.sync_api import expect
from actions.login_action import LoginActions


def load_test_data():
    data_path = Path(__file__).parent.parent / "data" / "login_data.json"
    with open(data_path, "r", encoding="utf-8") as file:
        return json.load(file)


TEST_DATA = load_test_data()
VALID_USER = TEST_DATA["valid_user"]
INVALID_INPUTS = TEST_DATA["invalid_inputs"]
EXPECTED_MESSAGES = TEST_DATA["expected_messages"]


@pytest.fixture
def login_actions(page):
    actions = LoginActions(page)
    actions.navigate_to_login()
    return actions


@allure.epic("Account Management")
@allure.feature("Login")
@allure.story("Form Validation")
@allure.title("Đăng nhập thất bại do để trống tất cả thông tin")
def test_empty_credentials(login_actions: LoginActions):
    
    # Action
    login_actions.click_empty_username()
    login_actions.press_enter()

    # Assert
    expect(login_actions.locators.username_error).to_have_text(
        EXPECTED_MESSAGES["empty_field"]
    )
    expect(login_actions.locators.password_error).to_have_text(
        EXPECTED_MESSAGES["empty_field"]
    )
    expect(login_actions.locators.login_button).to_be_disabled()


@allure.epic("Account Management")
@allure.feature("Login")
@allure.story("Form Validation")
@allure.title("Đăng nhập thất bại do sai định dạng Username")
@pytest.mark.parametrize(
    "input_key, expected_msg_key",
    [
        ("wrong_email_format", "invalid_email"),
        ("wrong_phone_format", "invalid_phone"),
    ],
    ids=["Invalid_Email_Format", "Invalid_Phone_Format"],
)
def test_invalid_username_format(
    login_actions: LoginActions, input_key, expected_msg_key
):
    
    # Action
    login_actions.fill_username(INVALID_INPUTS[input_key])
    login_actions.press_enter()
    
    # Assert
    expect(login_actions.locators.username_error).to_have_text(EXPECTED_MESSAGES[expected_msg_key])


@allure.epic("Account Management")
@allure.feature("Login")
@allure.story("Form Validation")
@allure.title("Đăng nhập thất bại do để trống Password")
def test_empty_password(login_actions: LoginActions):
    
    # Action
    login_actions.fill_username(VALID_USER["phone"])
    login_actions.click_empty_password()
    login_actions.press_enter()

    # Assert
    expect(login_actions.locators.password_error).to_have_text(
        EXPECTED_MESSAGES["empty_field"]
    )
    expect(login_actions.locators.login_button).to_be_disabled()


@allure.epic("Account Management")
@allure.feature("Login")
@allure.story("Invalid Login Luồng Chính")
@allure.title("Đăng nhập thất bại do sai Password")
def test_wrong_password(login_actions: LoginActions):
    
    # Action
    login_actions.fill_username(VALID_USER["phone"])
    login_actions.fill_password(INVALID_INPUTS["wrong_password"])
    login_actions.press_enter()
    
    # Assert
    expect(login_actions.locators.general_error).to_have_text(
        EXPECTED_MESSAGES["login_failed"]
    )


@allure.epic("Account Management")
@allure.feature("Login")
@allure.story("Valid Login Luồng Chính")
@allure.title("Đăng nhập thành công với tài khoản hợp lệ")
@allure.severity(allure.severity_level.CRITICAL)
def test_login_success(login_actions: LoginActions):
    
    # Action
    login_actions.fill_username(VALID_USER["phone"])
    login_actions.fill_password(VALID_USER["password"])
    login_actions.click_login_button()

    # Assert
    expect(login_actions.page).to_have_url(VALID_USER["expected_url"])
