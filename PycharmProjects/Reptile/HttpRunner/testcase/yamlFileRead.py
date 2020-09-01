import os.path
import yaml

print(os.path.abspath(__file__))
print(os.path.abspath('.'))
print(os.getcwd())

print(os.path.dirname(os.path.abspath(__file__)))
print(os.path.split(os.path.abspath(__file__)))


with open('./testYaml.yaml','r',encoding='utf-8') as f:
    print(f.read())
    loads = yaml.safe_load(f.read())
    print(loads)

print(yaml.safe_load(open("./testYaml.yaml",encoding='utf-8')))