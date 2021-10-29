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

@bot.message_handler(commands=['help'])
def help(message):
	bot.send_message(message.chat.id, "/start - Начало приключения \n /token - Добавить токен для отслеживания \n /boards - Посмотреть все доступные доски \n /trboards - посмотреть отслеживаваемые доски")

@bot.message_handler(commands=['start'])
def auth(message):
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

		user_login = first.get_your_login(data[1])

		db.set_user_token_data((message.chat.id, data[1], first.get_your_id(data[1]), user_login))

		bot.send_message(message.chat.id, "Вы успешно авторизовались!")
		bot.send_message(message.chat.id, "Выберите доски для отслеживания!", reply_markup = [inline_keyboard])
	else:
		bot.send_message(message.chat.id, "Проверьте токен и попробуйте еще раз!")

@bot.callback_query_handler(func=lambda c: c.data.split('%')[0] == '1')
def process_callback_boards_button(callback_query: CallbackQuery):

	data = callback_query.data.split('%')
	first.set_webhook(db.get_user_token_by_tele_token(callback_query.from_user.id), data[2])
	bot.answer_callback_query(callback_query.id)
	db.set_user_board_data((db.get_user_token_by_tele_token(callback_query.from_user.id), data[2]))
	bot.send_message(callback_query.from_user.id, f'Доска *{" ".join(data[1:len(data) - 1])}* успешно добавлена для отслеживания', parse_mode = 'Markdown')

@bot.message_handler(commands=['boards'])
def get_boards(message):

	inline_keyboard_small = InlineKeyboardMarkup()
	inline_keyboard_small = inline_keyboard_small.add(InlineKeyboardButton("Под наблюдением", callback_data = "in_data"))
	inline_keyboard_small = inline_keyboard_small.add(InlineKeyboardButton("Все доступные", callback_data = "all"))

	bot.send_message(message.chat.id, "Что именно хотелось бы узнать?", reply_markup = [inline_keyboard_small])

@bot.callback_query_handler(func=lambda c: c.data == 'in_data' or c.data == 'all')
def process_callback_boards_button(callback_query: CallbackQuery):
	if callback_query.data == 'all':
		boards = first.get_boards(db.get_user_token_by_tele_token(callback_query.message.chat.id))
		if boards != None:

			inline_keyboard = InlineKeyboardMarkup()
			for board in boards:
				inline_keyboard.add(InlineKeyboardButton(board['name'], callback_data = '1%' + board['name'] + '%' + board['id']))

			bot.send_message(callback_query.from_user.id, "Выберите доски для отслеживания!", reply_markup = [inline_keyboard])
		else:
			bot.send_message(callback_query.from_user.id, "Упс что-то пошло не так")

	if callback_query.data == 'in_data':
		boards = db.get_all_boards_by_token(db.get_user_token_by_tele_token(callback_query.message.chat.id))
		if boards != None:
			inline_keyboard = InlineKeyboardMarkup()
			for board in boards:
				board_name = first.get_boards_name_by_id(board[0], db.get_user_token_by_tele_token(callback_query.message.chat.id))
				inline_keyboard.add(InlineKeyboardButton(board_name, callback_data="pass"))
			bot.send_message(callback_query.from_user.id, "Вот что мне удалось найти", reply_markup = [inline_keyboard])
		else:
			bot.send_message(callback_query.from_user.id, "Там пока пустовато")


def send_info(data):
	print(data)

	if data.get('id'):
		res = db.get_user_token_and_tele_token_by_id(data['id'])
		bot.send_message(res[0], data['comment'])

	elif data.get('card'):

		tokens = db.get_tokens()
		for token in tokens:
			tmp = first.get_members_by_card_id(data['card'], token[0])
			if tmp != None:
				for elem in tmp:
					res = db.get_user_token_and_tele_token_by_id(elem)
					if res is not None:
						bot.send_message(res[0], data['comment'])

	elif data.get('users'):
		for user in data['users'][1:]:
			res = db.get_tele_token_by_login(user.rstrip())
			bot.send_message(res, data['comment'])

if __name__ == '__main__':
	bot.infinity_polling()
