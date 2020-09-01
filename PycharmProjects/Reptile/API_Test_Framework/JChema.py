import os.path
import yaml

print(os.path.abspath(__file__))
print(os.path.abspath('.'))
print(os.getcwd())

print(os.path.dirname(os.path.abspath(__file__)))
print(os.path.split(os.path.abspath(__file__)))

item = {}

with open('./desired_caps.yaml','r',encoding='utf-8') as f:
    print(f.readlines())
    # Loader = yaml.safe_load(f.read())
    # print(Loader)
    # print(item.update(Loader))

print(yaml.safe_load(open("./desired_caps.yaml",encoding='utf-8')))