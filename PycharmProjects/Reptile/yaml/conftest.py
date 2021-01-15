import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--cmdopt", action="store", default="{platformName:'Android',platformVersion:'5.1.1'}",
        help="my devices info"
    )


@pytest.fixture(scope="session")
def cmdopt(request):
    return request.config.getoption("--cmdopt")


@pytest.fixture
def start_app(cmdopt):
    device = eval(cmdopt)
    print("开始与设备 {} 进行会话，并执行测试用例 ！！".format(device["caps"]["deviceName"]))
    driver = start_appium_session(device)
    yield driver
    driver.close_app()
    driver.quit()