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
	bot.send_message(message.chat.id, "/start - Starting bot \n /token - Add trello token to the system \n /boards - Show all available boards ")

@bot.message_handler(commands=['start'])
def auth(message):
	bot.send_message(message.chat.id, "Welcome! Before proceeding, you must follow the link, copy the token from there and send it to me in the following format!  \n /token 123456789 ")
	bot.send_message(message.chat.id, 'https://trello.com/1/authorize?expiration=1day&name=MyPersonalToken&scope=read&response_type=token&key=193119f42d583601d5095b462bde9300')

@bot.message_handler(commands=['token'])
def token_accept(message):

	data = message.text.rstrip().split()
	if len(data) != 2:
		bot.send_message(message.chat.id, "Ooops, something went wrong please try again. \n /token 123456789")
		return
 
	boards = first.get_boards(data[1])
	if boards != None:

		inline_keyboard = InlineKeyboardMarkup()
		for board in boards:
			print(board['name'])
			inline_keyboard.add(InlineKeyboardButton(board['name'], callback_data = '1%' + board['name'] + '%' + board['id']))

		user_login = first.get_your_login(data[1])

		db.set_user_token_data((message.chat.id, data[1], first.get_your_id(data[1]), user_login))

		bot.send_message(message.chat.id, "You have successfully logged in!")
		bot.send_message(message.chat.id, "Select the boards to track!", reply_markup = [inline_keyboard])
	else:
		bot.send_message(message.chat.id, "Check the token and try again!")

@bot.callback_query_handler(func=lambda c: c.data.split('%')[0] == '1')
def process_callback_boards_button(callback_query: CallbackQuery):

	data = callback_query.data.split('%')
	first.set_webhook(db.get_user_token_by_tele_token(callback_query.from_user.id), data[2])
	bot.answer_callback_query(callback_query.id)
	db.set_user_board_data((db.get_user_token_by_tele_token(callback_query.from_user.id), data[2]))
	bot.send_message(callback_query.from_user.id, f'Board *{" ".join(data[1:len(data) - 1])}* successfully added for tracking', parse_mode = 'Markdown')

@bot.message_handler(commands=['boards'])
def get_boards(message):

	inline_keyboard_small = InlineKeyboardMarkup()
	inline_keyboard_small = inline_keyboard_small.add(InlineKeyboardButton("Tracking", callback_data = "in_data"))
	inline_keyboard_small = inline_keyboard_small.add(InlineKeyboardButton("All available", callback_data = "all"))

	bot.send_message(message.chat.id, "Whath do you want to know?", reply_markup = [inline_keyboard_small])

@bot.callback_query_handler(func=lambda c: c.data == 'in_data' or c.data == 'all')
def process_callback_boards_button(callback_query: CallbackQuery):
	if callback_query.data == 'all':
		boards = first.get_boards(db.get_user_token_by_tele_token(callback_query.message.chat.id))
		if boards != None:

			inline_keyboard = InlineKeyboardMarkup()
			for board in boards:
				inline_keyboard.add(InlineKeyboardButton(board['name'], callback_data = '1%' + board['name'] + '%' + board['id']))

			bot.send_message(callback_query.from_user.id, "Select the boards to track!", reply_markup = [inline_keyboard])
		else:
			bot.send_message(callback_query.from_user.id, "Ooops, something went wrong")

	if callback_query.data == 'in_data':
		boards = db.get_all_boards_by_token(db.get_user_token_by_tele_token(callback_query.message.chat.id))
		if boards != None:
			inline_keyboard = InlineKeyboardMarkup()
			i = 0
			for board in boards:
				board_name = first.get_boards_name_by_id(board[0], db.get_user_token_by_tele_token(callback_query.message.chat.id))
				inline_keyboard.add(InlineKeyboardButton(board_name, callback_data="pass" + str(i)))
			bot.send_message(callback_query.from_user.id, "That`s all I managed to find", reply_markup = [inline_keyboard])
		else:
			bot.send_message(callback_query.from_user.id, "Still empty")


def send_info(data):
	print(data)

	if data.get('id'):
		res = db.get_user_token_and_tele_token_by_id(data['id'])
		bot.send_message(res[0], data['comment'] + "Board name: " + data['board'])

	elif data.get('card'):

		tokens = db.get_tokens()
		for token in tokens:
			tmp = first.get_members_by_card_id(data['card'], token[0])
			if tmp != None:
				for elem in tmp:
					res = db.get_user_token_and_tele_token_by_id(elem)
					if res is not None:
						bot.send_message(res[0], data['comment'] + "Board name: " + data['board'])

	elif data.get('users'):
		for user in data['users'][1:]:
			res = db.get_tele_token_by_login(user.rstrip())
			bot.send_message(res, data['comment'] + "Board name: " + data['board'])

if __name__ == '__main__':
	bot.remove_webhook()
	bot.infinity_polling()
