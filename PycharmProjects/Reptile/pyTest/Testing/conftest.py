import pytest
from selenium import webdriver

'''
fixture里面的teardown用yield来唤醒teardown的执行
'''


@pytest.fixture(scope="module")
def login():
    a = 1
    print("输入账号，密码先登录")

    yield a
    print('执行teardown')
    print("最后关闭浏览器")


def pytest_addoption(parser):
    # 添加命令行选项,命令行传入参数"--cmdopt"
    parser.addoption(
        "--cmdopt", action="store", default="type1", help="my option: type1 or type2"
    )


@pytest.fixture
def cmdopt(request):
    return request.config.getoption("--cmdopt")





driver = None


# @pytest.mark.hookwrapper
# def pytest_runtest_makereport(item):
#     """
#     当测试失败的时候，自动截图，展示到html报告中
#     :param item:
#     """
#
#     pytest_html = item.config.pluginmanager.getplugin('html')

# 获取钩子方法的调用结果
#     outcome = yield
# 3. 从钩子方法的调用结果中获取测试报告
#     report = outcome.get_result()
#     extra = getattr(report, 'extra', [])
#
#     if report.when == 'call' or report.when == "setup":
#         xfail = hasattr(report, 'wasxfail')
#         if (report.skipped and xfail) or (report.failed and not xfail):
#             file_name = report.nodeid.replace("::", "_")+".png"
#             screen_img = _capture_screenshot()
#             if file_name:
#                 html = '<div><img src="data:image/png;base64,%s" alt="screenshot" style="width:600px;height:300px;" ' \
#                        'onclick="window.open(this.src)" align="right"/></div>' % screen_img
#                 extra.append(pytest_html.extras.html(html))
#         report.extra = extra


def _capture_screenshot():
    '''
    截图保存为base64，展示到html中
    :return:
    '''
    return driver.get_screenshot_as_base64()


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):
    print('---------------')
    out = yield
    report = out.get_result()
    print(report,'out:', out)
    if report.when == 'call':
        print(report.when)
        print(item.fixturenames)
        # print(item.funcargs["tmpdir"])
        print(report.nodeid)

@pytest.fixture(scope='function', autouse=True)
def browser(request):
    # 在request-context对象中注册addfinalizer方法也可以实现终结函数

    global driver
    if driver is None:
        driver = webdriver.Chrome()

    def end():
        driver.quit()
    request.addfinalizer(end)
    return driver
