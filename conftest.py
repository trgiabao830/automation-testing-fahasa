import os
import json
import allure
import pytest
from pathlib import Path
from playwright.sync_api import Playwright, Page

AUTH_FILE = ".auth/state.json"

pytest_plugins = ["utils.screenshot_hook"]


@pytest.fixture(scope="session", autouse=True)
def setup_auth_state(playwright: Playwright):
    """
    Fixture này tự động chạy 1 lần trước toàn bộ bộ test.
    Nhiệm vụ duy nhất của nó là tạo ra file state.json nếu chưa có.
    """
    if not os.path.exists(".auth"):
        os.makedirs(".auth")

    if not os.path.exists(AUTH_FILE):
        data_path = Path(__file__).parent / "data" / "login_data.json"
        with open(data_path, "r", encoding="utf-8") as file:
            login_data = json.load(file)

        valid_username = login_data["valid_user"]["phone"]
        valid_password = login_data["valid_user"]["password"]

        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://www.fahasa.com/")
        page.get_by_role("link", name="Tài khoản", exact=True).first.click()
        page.locator(".fhs-login-form #login_username").fill(valid_username)
        page.locator(".fhs-login-form #login_password").fill(valid_password)
        page.locator(".fhs-login-form #login_password").press("Enter")

        page.wait_for_url("https://www.fahasa.com/customer/account/")

        context.storage_state(path=AUTH_FILE)
        browser.close()


@pytest.fixture
def auth_page(browser):
    """
    Custom fixture cung cấp một "page" đã được nạp trạng thái đăng nhập.
    Chỉ test case nào gọi "auth_page" thì mới được đăng nhập sẵn.
    """
    # Tạo một context mới và nạp storage_state từ file
    context = browser.new_context(storage_state=AUTH_FILE)
    page = context.new_page()
    yield page
    context.close()