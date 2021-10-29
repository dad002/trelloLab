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