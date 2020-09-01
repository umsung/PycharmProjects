import requests
import os
import base64
import json

class RequestAPI(object):
    def send(self,data: dict):
        if data['schema'] == 'http':
            res = requests.request(data['method'],data['url'],headers = data['headers'])
            if data['encoding'] == 'base64':
                # print(json.loads(base64.b64decode(res.content)))
                return json.loads(base64.b64decode(res.content))
            elif data['encoding'] == 'private':
                return json.loads(requests.post("url", data=res.content).content)
            else:
                return json.loads(res.content)
        elif data['schema'] == 'dubbo':
            pass
        elif data['schema'] == 'websocket':
            pass
        else:
            pass
    