import requests
import json

yourKey = '193119f42d583601d5095b462bde9300'

def get_boards(yourToken):
    url = f'https://api.trello.com/1/members/me/boards?key={yourKey}&token={yourToken}'

    response = requests.request(
        "GET",
        url
    )

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return None

def set_webhook(yourToken):
    url = f"https://api.trello.com/1/webhooks?key={yourKey}&token={yourToken}"

    query = {
       'callbackURL': 'https://webhook.site/2b7777eb-281f-42dd-bc47-de665af148d8',
       'idModel': '616542590dfc3a27b9247b88'
    }

    response = requests.request(
       "POST",
       url,
       params=query
    )

    print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))

def get_your_id(yourToken):
    url = f'https://api.trello.com/1/members/me/?key={yourKey}&token={yourToken}'

    response = requests.request(
        "GET",
        url
    )

    if response.status_code == 200:
        return json.loads(response.text)['id']
    else:
        return None