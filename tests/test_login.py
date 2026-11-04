import json
import allure
import pytest
from pathlib import Path
from playwright.sync_api import expect
from pages.login_page import LoginActions


def load_test_data():
    data_path = Path(__file__).parent.parent / "data" / "login_data.json"
    with open(data_path, "r", encoding="utf-8") as file:
        return json.load(file)


TEST_DATA = load_test_data()


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
    login_actions.login()

    expect(login_actions.locators.username_error).to_have_text(
        TEST_DATA["expected_messages"]["empty_field"]
    )
    expect(login_actions.locators.password_error).to_have_text(
        TEST_DATA["expected_messages"]["empty_field"]
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
    invalid_input = TEST_DATA["invalid_inputs"][input_key]
    expected_msg = TEST_DATA["expected_messages"][expected_msg_key]

    login_actions.login(username=invalid_input)
    expect(login_actions.locators.username_error).to_have_text(expected_msg)


@allure.epic("Account Management")
@allure.feature("Login")
@allure.story("Form Validation")
@allure.title("Đăng nhập thất bại do để trống Password")
def test_empty_password(login_actions: LoginActions):
    login_actions.login(username=TEST_DATA["valid_user"]["phone"])

    expect(login_actions.locators.password_error).to_have_text(
        TEST_DATA["expected_messages"]["empty_field"]
    )
    expect(login_actions.locators.login_button).to_be_disabled()


@allure.epic("Account Management")
@allure.feature("Login")
@allure.story("Invalid Login Luồng Chính")
@allure.title("Đăng nhập thất bại do sai Password")
def test_wrong_password(login_actions: LoginActions):
    wrong_pwd = TEST_DATA["invalid_inputs"]["wrong_password"]

    login_actions.login(username=TEST_DATA["valid_user"]["phone"], password=wrong_pwd)
    expect(login_actions.locators.general_error).to_have_text(
        TEST_DATA["expected_messages"]["login_failed"]
    )


@allure.epic("Account Management")
@allure.feature("Login")
@allure.story("Valid Login Luồng Chính")
@allure.title("Đăng nhập thành công với tài khoản hợp lệ")
@allure.severity(allure.severity_level.CRITICAL)
def test_login_success(login_actions: LoginActions):
    login_actions.login(
        username=TEST_DATA["valid_user"]["phone"],
        password=TEST_DATA["valid_user"]["password"],
        submit_by="click",
    )

    expect(login_actions.page).to_have_url(TEST_DATA["valid_user"]["expected_url"])
