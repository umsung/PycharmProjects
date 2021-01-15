import time
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

options = Options()
# chrome_options.add_argument("--headless")
options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = Chrome(options=options)

# 打开能识别selenium页面前先运行这个stealth.min.js
with open('D:/Git/PycharmProjects/PycharmProjects/Reptile/seleniun_Learn/stealth.min.js') as f:
    js = f.read()

driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
  "source": js
})

# 老版Chrome + ChromeDriver 移除Selenium中的 window.navigator.webdriver
# driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
#   "source": """
#     Object.defineProperty(navigator, 'webdriver', {
#       get: () => undefined
#     })
#   """
# })
driver.get('https://www.aqistudy.cn/historydata/monthdata.php?city=%E5%8C%97%E4%BA%AC')
time.sleep(5)
driver.save_screenshot('walkaround.png')

# 你可以保存源代码为 html 再双击打开，查看完整结果
source = driver.page_source
with open('result.html', 'w') as f:
    f.write(source)