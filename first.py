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
       'callbackURL': 'https://trellostudy.herokuapp.com/webhook',
       'idModel': '5ebab65e0365003fd12a934c'
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

def get_your_login(yourToken):
    url = f'https://api.trello.com/1/members/me/?key={yourKey}&token={yourToken}'

    response = requests.request(
        "GET",
        url
    )

    if response.status_code == 200:
        return json.loads(response.text)['username']
    else:
        return None

def get_members_by_card_id(id, yourToken):
    url = f"https://api.trello.com/1/card/{id}/?key={yourKey}&token={yourToken}"

    response = requests.request(
        "GET",
        url
    )

    return json.loads(response.text)['idMembers'] if response.status_code == 200 else None

get_members_by_card_id('5ebab65e0365003fd12a934c', 'cfc80cc61a595690628b22b0fcf4a5a9dc86a8611588e45f5019a5269cb17446')