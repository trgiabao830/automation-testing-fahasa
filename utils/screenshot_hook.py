import os
import re
import allure
import pytest
from datetime import datetime

SCREENSHOT_DIR = "screenshots"

# Tự động tạo thư mục chứa ảnh nếu chưa tồn tại
os.makedirs(SCREENSHOT_DIR, exist_ok=True)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook này tự động chạy sau mỗi bước của một test case.
    Chụp ảnh màn hình (PASS/FAIL), format theo thời gian và đính kèm vào Allure.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        page = None

        for arg_name, arg_val in item.funcargs.items():
            if hasattr(arg_val, "page"):
                page = arg_val.page
                break
            elif arg_name in ["page", "auth_page"]:
                page = arg_val
                break

        if page:
            status = "FAIL" if report.failed else "PASS"
            timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
            safe_test_name = re.sub(r'[\\/*?:"<>|\[\]]', "_", item.name).strip("_")

            filename = f"{timestamp}_{status}_{safe_test_name}.png"
            file_path = os.path.join(SCREENSHOT_DIR, filename)

            page.screenshot(path=file_path, full_page=True)

            allure.attach.file(
                file_path,
                name=f"Screenshot_{status}",
                attachment_type=allure.attachment_type.PNG,
            )
