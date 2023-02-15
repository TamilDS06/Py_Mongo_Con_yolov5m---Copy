import requests
import json
from constant import constant

def api_log_in():
    try:
        url = constant.ROOT_URL+"device_login"
        response = None
        payload = json.dumps({
        "uuid": str(constant.uuid)
        })
        headers = {
        'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
    except Exception as exception:
        print("Error occurred during API_LOG_IN method", exception.args)
    finally:
        return response