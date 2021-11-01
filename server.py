from flask import Flask, request, abort
import json
import bot

print(bot.token)


DEV_KEY = '193119f42d583601d5095b462bde9300'

app = Flask(__name__)

user_token = ''

@app.route('/webhook', methods=['POST','HEAD'])
def webhook():
    print(request.method)
    if request.method == 'POST':

        res = {
            'action': request.json["action"]["type"],
            'comment': '',
            'board': '',
            'author': '',
            'user': ''
        }

        if res['action'] == 'updateCard':
            res['author'] = request.json['action']['memberCreator']['username']
            res['board'] = request.json['action']['data']['board']['name']
            if request.json['action']['data'].get('listBefore'):
                res['comment'] = f"{res['author']} moved your card from  {request.json['action']['data']['listBefore']['name']} to {request.json['action']['data']['listAfter']['name']}"
            elif request.json['action']['data'].get('old').get('name'):
                res['comment'] = f"{res['author']} changed your card name from {request.json['action']['data']['old']['name']} to {request.json['action']['data']['card']['name']} пользователем {res['author']}"
            elif request.json['action']['data'].get('old').get('due') != None:
                res['comment'] = f"{res['author']} changed your card time named {request.json['action']['data']['card']['name']} (deleting type)"
            elif request.json['action']['data'].get('old').get('due') == None:
                res['comment'] = f"{res['author']} changed your card time named {request.json['action']['data']['card']['name']} (adding type)"
            res['card'] = request.json['action']['data']['card']['id']

        elif res['action'] == 'removeMemberFromCard':
            res['author'] = request.json['action']['memberCreator']['username']
            res['board'] = request.json['action']['data']['board']['name']
            res['comment'] = f"You have been removed from the card {request.json['action']['data']['card']['name']} by user {res['author']}"
            res['id'] = request.json['action']['member']['id']

        elif res['action'] == 'addMemberToCard':
            res['author'] = request.json['action']['memberCreator']['username']
            res['board'] = request.json['action']['data']['board']['name']
            res['comment'] = f"You have been added to the card {request.json['action']['data']['card']['name']} by user {res['author']}"
            res['id'] = request.json['action']['member']['id']

        elif res['action'] == 'commentCard':
            res['author'] = request.json['action']['memberCreator']['username']
            res['users'] = request.json['action']['data']['text'].split('@')
            res['board'] = request.json['action']['data']['board']['name']
            res['comment'] = f"Your card has been commented {request.json['action']['data']['card']['name']}:\n{request.json['action']['data']['text']}\n{res['author']}"
        print(res)
        bot.send_info(res)
        

        return res, 200
    elif request.method == 'HEAD':
        print('connect')
        return 'success', 200
if __name__ == '__main__':
    app.run()