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

def set_webhook(yourToken, idModel):
    url = f"https://api.trello.com/1/webhooks?key={yourKey}&token={yourToken}"

    query = {
       'callbackURL': 'https://trelloappstudy.herokuapp.com/webhook',
       'idModel': {idModel}
    }

    response = requests.request(
       "POST",
       url,
       params=query
    )

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

def get_boards_name_by_id(id, yourToken):
    url = f"https://api.trello.com/1/board/{id}/?key={yourKey}&token={yourToken}"

    response = requests.request(
        "GET",
        url
    )

    return json.loads(response.text)['name'] if response.status_code == 200 else None