import json
import requests
from src.Parser import Parser
import time

SERVER_IP = "aibg2022.com:8081"

def get_action(action):
    body_action = {
        "action": action
    }
    return body_action

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    with open('cred.json', 'r') as file:
        bot_number = 1 #input("Bot number: ")
        content = json.loads(file.read())
        content["username"] = content["username"] + str(bot_number)
        #print(content["username"])

        # send the content directly to the server

        headers = {
            'Content-Type': 'application/json'
        }

        url = "http://" + SERVER_IP + "/user/login"
        #print(url)

        res = requests.post(url=url, headers=headers, data=json.dumps(content))
        #print(res.json())
        token = res.json()["token"]


    #print(token)

    # Za testriranje:
    #url = "http://" + SERVER_IP + "/game/train"

    #headers = {
    #    'Authorization': 'Bearer ' + token,
    #    'Content-Type': 'application/json',
    #}

    #print(headers)
    #print("http://" + SERVER_IP + "/game/actionTrain")

    #playerIdx = 1

    #data = {
    #    "mapName": "test2.txt",
    #    "playerIdx": playerIdx,
    #    "time": 1
    #}


    #res = requests.post(url=url, headers=headers, data=json.dumps(data)).json()
    #print(res)
    #game_state = res['gameState']

    # test
    #game_state = res["gameState"]


    # za create game:

    # url = "http://" + SERVER_IP + "/game/createGame"
    # headers = {
    #     'Authorization': 'Bearer ' + token,
    #     'Content-Type': 'application/json'
    # }
    #
    # data = {
    #     "playerUsernames": ["BotDiff1", "BotDiff2", "BotDiff3", "BotDiff4"],
    #     "mapName": "test2.txt",
    #     "time": 1
    # }
    #
    # res = requests.post(url=url, headers=headers, data=json.dumps(data))
    #
    # print("Create game!")
    # print(res.json())

    # Za igranje igre:

    url = "http://" + SERVER_IP + "/game/joinGame"
    headers = {
        'Authorization': 'Bearer: ' + token,
    }
    #print("JOIN GAME")
    #print(url)
    #print(headers)
    res = requests.get(url=url, headers=headers)
    res_json = res.json()

    #print(res_json)

    game_state = res_json['gameState']
    #print(game_state)
    idxPlayer = res_json["playerIdx"]
    #parser = Parser(idxPlayer)
    parser = Parser(idxPlayer)

    #print(game_state)
    #time.sleep(6)


    while True:
        # dobijanje statea
        time_first = time.time()
        # sleep

        # calculate what to do => chose between move and action
        #print(game_state)
        action = parser.getBestMove(state=json.loads(game_state))
        #print(action)
        body = get_action(action)

        url = "http://" + SERVER_IP + "/game/doAction/"

        headers = {
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json',
        }

        res = requests.post(url=url, headers=headers, data=json.dumps(body))
        #print(json.dumps(body))
        #print(url)
        #print(headers)
        #print(res.json())

        if not res:
            break
        game_state = res.json()["gameState"]

        #print("Vreme potoroseno")
        delta = 0.2
        time_left = 3 - (time.time() - time_first)

        #print(time_left)

        if time_left - delta > 0:
            time.sleep(time_left - delta)
        # igranje partije
        # doAction || actionTrain

        #print(time.time() - time_first)


