import telebot
import first
import database
from aiogram.types import ReplyKeyboardRemove, \
	ReplyKeyboardMarkup, KeyboardButton, \
	InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

token = "2089522410:AAHkzYGGd3X76IBzLNP--Pp2xLIAAAZsVjM"

db = database.DataBase()
db.create_tables()

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def auth(message):
	print(message.chat.id)
	bot.send_message(message.chat.id, "Добро пожаловать! Прежде чем приступить вы должны перейти по ссылке, скопировать оттуда токен и отправить мне в следующем формате! \n /token 123456789 ")
	bot.send_message(message.chat.id, 'https://trello.com/1/authorize?expiration=1day&name=MyPersonalToken&scope=read&response_type=token&key=193119f42d583601d5095b462bde9300')

@bot.message_handler(commands=['token'])
def token_accept(message):

	data = message.text.rstrip().split()
	if len(data) != 2:
		bot.send_message(message.chat.id, "Что-то пошло не так, попробуйте ввести еще раз в следующем формате! \n /token 123456789")
		return

	boards = first.get_boards(data[1])
	if boards != None:

		inline_keyboard = InlineKeyboardMarkup()
		for board in boards:
			inline_keyboard.add(InlineKeyboardButton(board['name'], callback_data = '1%' + board['name'] + '%' + board['id']))

		db.set_user_token_data((message.chat.id, data[1], first.get_your_id(data[1])))

		first.set_webhook(data[1])

		bot.send_message(message.chat.id, "Вы успешно авторизовались!")
		bot.send_message(message.chat.id, "Выберите доски для отслеживания!", reply_markup = [inline_keyboard])
	else:
		bot.send_message(message.chat.id, "Проверьте токен и попробуйте еще раз!")

@bot.callback_query_handler(func=lambda c: c.data.split('%')[0] == '1')
def process_callback_boards_button(callback_query: CallbackQuery):
	data = callback_query.data.split('%')
	bot.answer_callback_query(callback_query)
	db.set_user_board_data((db.get_user_token_by_tele_token(callback_query.chat.id), data[2]))
	bot.send_message(callback_query.from_user.id, f'Доска *{" ".join(data[1:len(data) - 1])}* успешно добавлена для отслеживания', parse_mode = 'Markdown')


def send_info(data):
	if data.get('id'):
		res = db.get_user_token_and_tele_token_by_id(data['id'])
		bot.send_message(res[0], data['comment'])
	elif data.get('card'):
		pass
	elif data.get('users'):
		for user in data['users'][1:]:
			user.rstrip()
			print(user)

if __name__ == '__main__':
	bot.infinity_polling()
