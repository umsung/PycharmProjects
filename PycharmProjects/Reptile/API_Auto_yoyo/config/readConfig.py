import os
import configparser


cur_path = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(cur_path, 'cfg.ini')
config = configparser.ConfigParser()
config.read(config_path)


stmp_server = config.get('email', 'stmp_server')
port = config.get('email', 'port')

sender = config.get('email', 'sender')
receiver = config.get('email', 'receiver')      # 多个收件人用逗号割开

pwd = config.get('email', 'pwd')