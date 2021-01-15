import os
import time
import pytest
import yaml
from selenium import webdriver
import subprocess
from concurrent.futures import ThreadPoolExecutor


print(os.path.abspath(__file__))
print(os.path.abspath('.'))

# 设备启动参数配置文件
basepath = os.path.join(os.path.join(os.path.abspath('.'), 'pageelement'), 'desired_caps.yaml')
desired_template_path = os.path.join(os.path.join(os.path.abspath('.'), 'pageelement'), 'desired_template.yaml')
print(basepath)

class ManageAppiumServer:
    """
    appium desktop通过命令行启动appium服务。
    不同平台上安装的appium，默认的appium服务路径不一样。
    初始化时，设置appium服务启动路径
    再根据给定的端口号启动appium
    """

    def __init__(self,appium_server_apth):
        self.server_apth = appium_server_apth

    # 启动appium server服务
    def start_appium_server(self,port=4723):
        appium_log_path = os.path.join(os.path.join(os.path.abspath('.')),"appium_server_{0}.log".format(port))
        command = "node {0} -p {1} -g {2} " \
                  "--session-override " \
                  "--local-timezone " \
                  "--log-timestamp & ".format(self.server_apth, port, appium_log_path)
        subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True).communicate()

    # 关闭appium服务
    @classmethod
    def stop_appium(cls,pc,post_num=4723):
        '''关闭appium服务'''
        if pc.upper() == 'WIN':
            p = os.popen(f'netstat  -aon|findstr {post_num}')
            p0 = p.read().strip()
            if p0 != '' and 'LISTENING' in p0:
                p1 = int(p0.split('LISTENING')[1].strip()[0:4])  # 获取进程号
                os.popen(f'taskkill /F /PID {p1}')  # 结束进程
                print('appium server已结束')
        elif pc.upper() == 'MAC':
            p = os.popen(f'lsof -i tcp:{post_num}')
            p0 = p.read()
            if p0.strip() != '':
                p1 = int(p0.split('\n')[1].split()[1])  # 获取进程号
                os.popen(f'kill {p1}')  # 结束进程
                print('appium server已结束')

class ManageDevices:
    """
       1、重启adb服务。
       2、通过adb devices命令获取当前平台中,已连接的设备个数，和设备uuid.
       3、通过adb -P 5037 -s 设备uuid shell getprop ro.build.version.release获取每一个设备的版本号。
       4、将所有已连接设备的设备名称、设备版本号存储在一个列表当中。
       5、通过调用get_devices_info函数，即可获得4中的列表。
    """

    def __init__(self):
        # self.__devices_info = []
        # 重启adb服务
        os.system("adb kill-server")
        os.system("adb start-server")

    def __get_devices_uuid(self):
        devicesInfoLists = os.popen('adb devices').read().split('\n')[1:]
        devicesInfoListsNoNull = list(filter(None,devicesInfoLists))
        d = {}
        desired_caps = []
        for item in devicesInfoListsNoNull:
            d['uid'] = item.split('\t')[0]
            d['name'] = item.split('\t')[1]
            desired_caps.append(d)
        return desired_caps

    def __get_device_platform_vesion(self):
        pass

    def __devices_info(self):
        # 获取各连接设备的名称，uid等
        devicesInfoLists = os.popen('adb devices').read().split('\n')[1:]
        devicesInfoListsNoNull = list(filter(None,devicesInfoLists))
        d = {}
        desired_caps = []
        for item in devicesInfoListsNoNull:
            d['uuid'] = item.split('\t')[0]
            d['deviceName'] = item.split('\t')[1]
            desired_caps.append(d)
        return desired_caps

    def get_devices_info(self):
        """
        获取已连接设备的uuid,和版本号。
        :return: 所有已连接设备的uuid,和版本号。
        """
        self.__get_devices_uuid()
        print(self.__devices_info)
        self.__get_device_platform_vesion()
        return self.__devices_info

    def __get_yaml_data(self):
        f = open(desired_template_path, 'r', encoding='utf-8')
        # 存储了启动参数模板
        a = f.read()
        dict_content = yaml.load(a)
        return dict_content[0]


    def devices_pool(self,port=4723,system_port=8200):
        """
        动态生成设备启动参数管理池。含启动参数和对应的端口号
        :param port: appium服务的端口号。每一个设备对应一个。
        :param system_port: appium服务指定的本地端口，用来转发数据给安卓设备。每一个设备对应一个。
        :return: 所有已连接设备的启动参数和appium端口号。
        """
        
        devs_pool = []
        # 获取当前连接的所有设备信息
    
        desired_template = self.__get_yaml_data()
        all_devices_info = self.get_devices_info()
        # 补充每一个设备的启动信息，以及配置对应的appium server端口号
        if all_devices_info:
            for dev_info in all_devices_info:
                dev_info.update(desired_template)
                dev_info["systemPort"] = system_port
                new_dict = {
                    "caps": dev_info,
                    "port": port
                }
                devs_pool.append(new_dict)
                port += 4
                system_port += 4
        return devs_pool



# 根据设备启动信息，通过pytest.main来收集并执行用例。
# pytest 的命令行参数。
# 首先需要在 conftest.py 添加命令行选项，命令行传入参数”--cmdopt“。用例如果需要用到从命令行传入的参数，就调用 cmdopt 函数
def run_cases(device):
    """
    参数：device为设备启动参数。在pytest.main当中，传递给--cmdopt选项。
    """
    print(["-s", "-v", "--cmdopt={}".format(device)])
    reports_path = os.path.join('.',"test_result_{}_{}.html".format(device["caps"]["deviceName"], device["port"]))
    pytest.main(["-s", "-v",
                 "--cmdopt={}".format(device),
                 "--html={}".format(reports_path)]
                )

m = ManageDevices()
# 第一步：从设备池当中，获取当前连接的设备。若设备池为空，则无设备连接。
devices = m.devices_pool()
platform_name = ''
appium_server_path = ''
# 第二步：若设备池不为空，启动appium server.与设备个数对应。起始server端口为4723，每多一个设备，端口号默认+4
if devices and platform_name and appium_server_path:
    # 创建线程池
    T = ThreadPoolExecutor()
    # 实例化appium服务管理类。
    mas = ManageAppiumServer(appium_server_path)
    for device in devices:
        # kill 端口，以免占用
        mas.stop_appium(platform_name,device["port"])
        # 启动appium server
        task = T.submit(mas.start_appium_server,device["port"])
        time.sleep(1)

    # 第三步：若设备池不为空，在appium server启动的情况下，执行app自动化测试。
    time.sleep(15)
    obj_list = []
    for device in devices:
        index = devices.index(device)
        task = T.submit(run_cases,device)
        obj_list.append(task)
        time.sleep(1)

    # 等待自动化任务执行完成
    for future in as_completed(obj_list):
        data = future.result()
        print(f"sub_thread: {data}")

    # kill 掉appium server服务,释放端口。
    for device in devices:
        ManageAppiumServer.stop_appium(platform_name, device["port"])













# ---------------------------------------------



def get_desired_caps(deviceName=''):
    '''
       t = {"token": value}
       with open(ypath, "w", encoding="utf-8") as f:
           yaml.dump(t, f, Dumper=yaml.RoundTripDumper)
        获取配置文件的所有启动参数，再为每个设备启动不同端口的appium服务
       '''

    f = open(basepath, 'r', encoding='utf-8')
    a = f.read()
    dict_content = yaml.load(a)
    # dict_content = yaml.safe_load(open(basepath))
    print(dict_content)
    for i in dict_content:
        if deviceName in i['desc']:
            strat_appium_server(i['port'], i['desired_caps']['uuid'])
            return i['desired_caps'], i['port']


def strat_appium_server(port='', uuid=''):
    r = os.popen('netstat -ano | findstr "%s" ' % port)
    time.sleep()
    result = r.read()
    if 'LISTENING' in result:
        print('appium服务已启动')
    else:
        os.system('appium -a 127.0.0.1 -p %s -u %s --no-reset' % (port, uuid))


def run_app(deviceName):
    desired_caps = get_desired_caps(deviceName)[0]
    driver = webdriver.Remote('https://127.0.0.1:%s/wd/hub', desired_caps)
    driver.find_element_by_id('').click()
    driver.find_element_by_xpath('').send_keys('')



def kill_app(package_name):
    """
    关闭指定的应用
    :param package_name：例如东方头条【com.songheng.eastnews】
    :return:
    """
    # nowtime = os.popen('date')
    # print(nowtime.read())
    os.popen('adb shell am force-stop %s' % package_name)


def start_my_app(package_name, activity_name):
    """
    打开应用
    adb shell am start -n com.tencent.mm/.ui.LauncherUI
    :param package_name:
    :return:
    """
    os.popen('adb shell am start -n %s/%s' % (package_name, activity_name))


def kill_all():
    """
    关闭所有的应用
    :return:
    """
    os.popen('adb shell am kill-all')


if __name__ == '__main__':
    run_app('夜神')