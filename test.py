import requests
import json

r = requests.get('https://sr-api.sfirew.com/server/whatisthis.myddns.me')
doc = json.loads(r.text)

if r.status_code == requests.codes.ok:
    if doc['online']:
        playerCount = doc['players']['online']
        players = []
        count = 0
        for i in doc['players']['sample']:
            players.append(doc['players']['sample'][count]['name'])
            count = count + 1

        print(f"伺服器上線中。\n目前上線玩家數：{playerCount}\n目前上線玩家：")
        for j in players:
            print(j)
    else:
        print("伺服器離線。")
else:
    print("伺服器無法存取資料。")