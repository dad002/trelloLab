import requests
import json

yourKey = '193119f42d583601d5095b462bde9300'
yourToken = '051f6534202857a75e06a3c58358840f62a4e54fe268648aad672465cb2cb4c6'

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