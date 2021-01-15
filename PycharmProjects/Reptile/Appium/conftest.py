import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--cmdopt", action="store", default="{platformName:'Android',platformVersion:'5.1.1'}",
        help="my devices info"
    )


@pytest.fixture(scope="session")
def cmdopt(request):
    return request.config.getoption("--cmdopt")

# module级别每个.py文件执行一次, autouse默认值是false，设置为true，所有作用域内的测试用例都会自动调用该fixture
@pytest.fixture(scope="module", autouse=False)
def start_app(cmdopt):
    device = eval(cmdopt)
    print("开始与设备 {} 进行会话，并执行测试用例 ！！".format(device["caps"]["deviceName"]))
    driver = start_appium_session(device)
    yield driver
    driver.close_app()
    driver.quit()


def start_appium_session(device):
    desired_caps = device['dev_info']
    driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub',desired_caps)
    driver.implicitly_wait(2)
    return driver