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
        bot.send_info(123)

        res = {
            'action': request.json['action']['type'],
            'comment': '',
            'board': request.json['action']['data']['board']['name'],
            'list': request.json['action']['data']['list']['name'],
            'author': request.json['action']['memberCreator']['username']
        }

        comment = ''

        if res['action'] == 'updateCard':            
            if request.json['action']['data'].get('listBefore'):
                comment = f"Вас переместил {res['author']} из листа {request.json['action']['data']['listBefore']['name']} в {request.json['action']['data']['listAfter']['name']}"
            elif request.json['action']['data'].get('old'):
                comment = f"Название вашей карточки {request.json['action']['data']['old']} изменилось на {request.json['action']['data']['card']['name']} пользователем {res['author']}"

        elif res['action'] == 'removeMemberFromCard':
            comment = f"Вы удалены из карточки {request.json['action']['data']['card']['name']} пользователем {res['author']}"

        elif res['action'] == 'addMemberToCard':
            comment = f"Вы добавлены в карточку {request.json['action']['data']['card']['name']} пользователем {res['author']}"

        elif res['action'] == 'commentCard':
            comment = f"Комментарий к вашей карточке {request.json['action']['data']['card']['name']}:\n{request.json['action']['data']['text']}\n{res['author']}"


        res['comment'] = comment

        return res, 200
    elif request.method == 'HEAD':
        print('connect')
        return 'success', 200
if __name__ == '__main__':
    app.run()