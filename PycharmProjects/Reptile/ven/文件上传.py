import requests
import json

def uploadFile():
    data = {
        "bName":"",
        "fName":"",
        "fileName":[]

    }

    files = {
        "file1":open(r"./1.png","rb"),
        "file2":open(r"./2.png","rb")
    }

    url =""

    response = requests.post(url = url, data= data, files = files)
    print(response.json())