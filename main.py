import json
import requests
from src.Parser import Parser
import time

SERVER_IP = "aibg22.com:8081"

def get_action(action):
    body_action = {
        "action": action
    }
    return body_action

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
        print(res.json())
        token = res.json()["token"]

    #print(token)

    # Za testriranje:
    url = "http://" + SERVER_IP + "/game/train"

    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json',
    }

    #print(headers)
    #print("http://" + SERVER_IP + "/game/actionTrain")

    playerIdx = 1

    data = {
        "mapName": "test2.txt",
        "playerIdx": playerIdx,
        "time": 1
    }


    res = requests.post(url=url, headers=headers, data=json.dumps(data)).json()
    print(res)
    #game_state = res['gameState']

    # test
    #idxPlayer = res["playerIdx"]
    game_state = res["gameState"]

    parser = Parser(playerIdx)
    #print(parser.getBestMove(state=game_state["gameState"].json()))

    # Za igranje igre:

    #url = "http://" + SERVER_IP + "/game/joinGame"
    #headers = {
    #    'Authorization': 'Bearer ' + token
    #}
    #print(url)
    #print(headers)
    #res = requests.get(url=url, headers=headers)
    #print(res.json())


    time.sleep(6)

    while True:
        # dobijanje statea
        time_first = time.time()
        # sleep

        # calculate what to do => chose between move and action
        #print(game_state)
        action = parser.getBestMove(state=json.loads(game_state))
        print(action)
        body = get_action(action)

        url = "http://" + SERVER_IP + "/game/actionTrain"

        header = {
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json',
        }

        res = requests.post(url=url, headers=headers, data=json.dumps(body))

        if not res:
            break
        game_state = res.json()["gameState"]

        print("Vreme potoroseno")
        delta = 0.2
        time_left = 3 - (time.time() - time_first)

        #time.sleep(time_left - delta)
        # igranje partije
#         # doAction || actionTrain

        print(time.time() - time_first)


