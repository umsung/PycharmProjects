import asyncio
import random
import time
from pyppeteer import launch
from retrying import retry


async def taobao_login(username, password, url):
    """
    淘宝登录主程序
    :param username: 用户名
    :param password: 密码
    :param url: 登录网址
    :return: 登录cookies
    """
    # 'headless': False如果想要浏览器隐藏更改False为True
    browser = await launch({'headless': False, 'args': ['--no-sandbox']})
    page = await browser.newPage()
    # await page.setJavaScriptEnabled(enabled=False)
    await page.setUserAgent(
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36')
    await page.goto(url)

    # 以下为插入中间js，将淘宝会为了检测浏览器而调用的js修改其结果
    await page.evaluate(
        '''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''')
    await page.evaluate('''() =>{ window.navigator.chrome = { runtime: {},  }; }''')
    await page.evaluate('''() =>{ Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] }); }''')
    await page.evaluate('''() =>{ Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5,6], }); }''')

    await page.click('#J_QRCodeLogin > div.login-links > a.forget-pwd.J_Quick2Static')
    page.mouse
    time.sleep(1)
    # 输入用户名，密码
    await page.type('#TPL_username_1', username)   # delay是限制输入的时间
    time.sleep(random.uniform(1,1.5))
    await page.type('#TPL_password_1', password)
    time.sleep(random.uniform(0,1))
    # 检测页面是否有滑块。原理是检测页面元素。
    slider = await page.Jeval('#nocaptcha', 'node => node.style')  # 是否有滑块

    if slider:
        print('当前页面出现滑块')
        # await page.screenshot({'path': './headless-login-slide.png'}) # 截图测试
        flag, page = await mouse_slide(page=page)  # js拉动滑块过去。
        if flag:
            await page.evaluate('''document.getElementById("J_SubmitStatic").click()''')  # 如果无法通过回车键完成点击，就调用js模拟点击登录按钮。
            time.sleep(2)
            cookies_list = await page.cookies()
            print(cookies_list)
            cookie=await get_cookie(page)
            return  cookie   # 导出cookie 。
    else:
        await page.evaluate('''document.getElementById("J_SubmitStatic").click()''')
        await page.waitFor(20)
        await page.waitForNavigation()
        cookie=await get_cookie(page)

        return  cookie


# 获取登录后cookie
async def get_cookie(page):
    # res = await page.content()
    cookies_list = await page.cookies()
    cookies = ''
    for cookie in cookies_list:
        str_cookie = '{0}={1};'
        str_cookie = str_cookie.format(cookie.get('name'), cookie.get('value'))
        cookies += str_cookie
    return cookies


def retry_if_result_none(result):
    return result is None


@retry(retry_on_result=retry_if_result_none)
async def mouse_slide(page=None):
    time.sleep(3)
    await asyncio.sleep(2)
    try:
        # 鼠标移动到滑块，按下，滑动到头（然后延时处理），松开按键
        await page.hover('#nc_1_n1z')  # 不同场景的验证码模块能名字不同。
        await page.mouse.down()
        await page.mouse.move(2000, 0, {'delay': random.randint(1000, 2000)})
        await page.mouse.up()
        print('滑动完成')
    except Exception as e:
        print(e, ':验证失败')
        return None, page
    else:
        await asyncio.sleep(2)
        # 判断是否通过
        slider_again = await page.Jeval('.nc-lang-cnt', 'node => node.textContent')
        print(slider_again)
        if slider_again != '验证通过':
            return None, page
        else:
            print('验证通过')
            return 1, page





if __name__ == '__main__':
    try:
        time1=time.time()
        username = ''
        password = ''
        url = 'https://login.taobao.com/member/login.jhtml?redirectURL=https%3A%2F%2Fwww.taobao.com%2F'
        loop = asyncio.get_event_loop()
        task = asyncio.ensure_future(taobao_login(username, password, url))
        loop.run_until_complete(task)
        cookie = task.result()
        print(cookie)
        time2=time.time()
        print(time2-time1)
    except:
        print('os error')