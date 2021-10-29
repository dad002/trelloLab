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

@bot.message_handler(commands=['trboards'])
def get_boards(message):
	token = db.get_user_token_by_tele_token(message.from_user.id)
	res = db.get_all_boards_by_token(token)

	inline_keyboard = InlineKeyboardMarkup()
	for board in res:
		board_tmp = first.get_boards_name_by_id(board[0], token)
		inline_keyboard.add(InlineKeyboardButton(board_tmp, callback_data = '1%' + board_tmp + '%' + board_tmp))
	bot.send_message(message.chat.id, "Доски активно отслеживаваемые в данный момент!", reply_markup = [inline_keyboard])

@bot.message_handler(commands=['boards'])
def get_boards(message):
	res = db.get_user_token_by_tele_token(message.from_user.id)
	res = first.get_boards(res)

	inline_keyboard = InlineKeyboardMarkup()
	for board in res:
		inline_keyboard.add(InlineKeyboardButton(board['name'], callback_data = '1%' + board['name'] + '%' + board['id']))
	bot.send_message(message.chat.id, "Доски активно отслеживаваемые в данный момент!", reply_markup = [inline_keyboard])

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
