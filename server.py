from flask import Flask, request, abort
import json
import bot

print(bot.token)


DEV_KEY = '193119f42d583601d5095b462bde9300'

app = Flask(__name__)

user_token = ''

@app.route('/webhook', methods=['POST','HEAD'])
def webhook():
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
                res['comment'] = f"Вас переместил {res['author']} из листа {request.json['action']['data']['listBefore']['name']} в {request.json['action']['data']['listAfter']['name']}"
            elif request.json['action']['data'].get('old').get('name'):
                res['comment'] = f"Название вашей карточки {request.json['action']['data']['old']['name']} изменилось на {request.json['action']['data']['card']['name']} пользователем {res['author']}"
            elif request.json['action']['data'].get('old').get('dueReminder'):
                res['comment'] = f"Время вашей карточки {request.json['action']['data']['card']['name']} было удалено пользователем {res['author']}"
            elif request.json['action']['data'].get('old').get('due'):
                res['comment'] = f"На вашей карточке {request.json['action']['data']['card']['name']} было уставновлено время пользователем {res['author']}"
            res['card'] = request.json['action']['data']['card']

        elif res['action'] == 'removeMemberFromCard':
            res['author'] = request.json['action']['memberCreator']['username']
            res['board'] = request.json['action']['data']['board']['name']
            res['comment'] = f"Вы удалены из карточки {request.json['action']['data']['card']['name']} пользователем {res['author']}"
            res['id'] = requests.json['action']['member']['id']

        elif res['action'] == 'addMemberToCard':
            res['author'] = request.json['action']['memberCreator']['username']
            res['board'] = request.json['action']['data']['board']['name']
            res['comment'] = f"Вы добавлены в карточку {request.json['action']['data']['card']['name']} пользователем {res['author']}"
            res['id'] = requests.json['action']['member']['id']

        elif res['action'] == 'commentCard':
            res['author'] = request.json['action']['memberCreator']['username']
            res['users'] = request.json['action']['data']['text'].split('@')
            res['board'] = request.json['action']['data']['board']['name']
            res['comment'] = f"Комментарий к вашей карточке {request.json['action']['data']['card']['name']}:\n{request.json['action']['data']['text']}\n{res['author']}"

        print(res)
        print('----------')
        bot.send_info(res)
        

        return res, 200
    elif request.method == 'HEAD':
        print('connect')
        return 'success', 200
if __name__ == '__main__':
    app.run()