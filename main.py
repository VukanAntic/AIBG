import json
import requests
import time

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

    #print(token)

    # Za testriranje:
    url = "http://" + SERVER_IP + "/game/train"

    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json',
    }

    data = {
        "mapName": "test1.txt",
        "playerIdx": 1,
        "time": 1
    }

    res = requests.post(url=url, headers=headers, data=json.dumps(data)).json()
    game_state = res['gameState']

    #parser = Parser()

    # Za igranje igre:

    # url = "http://" + SERVER_IP + "/game/joinGame"
    # headers = {
    #     'Authorization': 'Bearer ' + token
    # }
    # print(url)
    # print(headers)
    # res = requests.get(url=url, headers=headers)
    # print(res.json())

    while True:
        # dobijanje statea
        # body = parser.getBestMove(game_state)
        # sleep
        # up to debate
        time.sleep(2800)

        # calculate what to do => chose between move and action

        # when we stop training, /game/doAction
        url = "http://" + SERVER_IP + "/game/actionTrain"

        header = {
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json',
        }

        res = requests.post(url=url, headers=headers, data=json.dumps(body))

        game_state = res.json()["gameState"]


