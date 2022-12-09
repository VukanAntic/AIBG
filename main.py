# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import json
import requests

SERVER_IP = "aibg22.com:8081"



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    with open('cred.json', 'r') as file:
        content = file.read()

        # send the content directly to the server

        headers = {
            'Content-Type': 'application/json'
        }

        url = "http://" + SERVER_IP + "/user/login"
        #print(url)

        res = requests.post(url=url, headers=headers, data=content)
        token = res.json()["token"]

    print(token)

    # Za testriranje:
    url = "http://" + SERVER_IP + "/game/train"

    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json',
    }

    data = {
        "mapName": "test1.txt",
        "playerIdx": 1
    }

    print(requests.post(url=url, headers=headers, data=json.dumps(data)).json())



    # Za igranje igre:

    url = "http://" + SERVER_IP + "/game/joinGame"
    headers = {
        'Authorization': 'Bearer ' + token
    }
    print(url)
    print(headers)
    res = requests.get(url=url, headers=headers)
    print(res.json())







