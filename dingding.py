import requests
import json


headers = {"Content-Type": "application/json"}

def ding_text(apiurl, content):
    msg = {"msgtype": "text", "text": content}
    requests.post(apiurl, headers=headers, data=json.dumps(msg))
