import sqlite3

class DataBase:

    def __init__(self):
        self.con = sqlite3.connect('data.db', check_same_thread=False)
        self.cur = self.con.cursor()


    def create_tables(self):

        self.cur.execute("""CREATE TABLE IF NOT EXISTS user_token (tele_token TEXT, user_token TEXT, user_id TEXT, user_login TEXT)""")
        self.cur.execute("""CREATE TABLE IF NOT EXISTS user_boards (user_token TEXT, board_id TEXT)""")
        self.cur.execute("""CREATE TABLE IF NOT EXISTS board_info (board_id TEXT, message_type INTEGER)""")


    def set_user_token_data(self, data):
        print('user', data)

        self.cur.execute(f"""INSERT INTO user_token (tele_token, user_token, user_id, user_login) 
            SELECT '{data[0]}', '{data[1]}', '{data[2]}', '{data[3]}' 
            WHERE NOT EXISTS 
            (SELECT 1 FROM user_token WHERE tele_token='{data[0]}' AND user_token='{data[1]}' AND user_id='{data[2]}' AND user_login='{data[3]}')""")
        self.con.commit()

    def set_user_board_data(self, data):
        print(data)

        self.cur.execute(f"""INSERT INTO user_boards (user_token, board_id) 
            SELECT '{data[0]}', '{data[1]}' 
            WHERE NOT EXISTS 
            (SELECT 1 FROM user_boards WHERE user_token='{data[0]}' AND board_id='{data[1]}')""")
        self.con.commit()

    def set_board_info_data(self, data):

        self.cur.execute(f"""INSERT INTO board_info (board_id, message_type) 
            SELECT '{data[0]}', '{data[1]}' 
            WHERE NOT EXISTS 
            (SELECT 1 FROM board_info WHERE board_id='{data[0]}' AND message_type='{data[1]}')""")
        self.con.commit()

    def get_user_token_by_tele_token(self,token):
        tmp = self.cur.execute(f"""SELECT user_token FROM user_token WHERE tele_token='{token}'""").fetchone()
        return tmp[0] if tmp is not None else None

    def get_user_token_and_tele_token_by_id(self, id):
        return self.cur.execute(f"SELECT tele_token, user_token FROM user_token WHERE user_id = '{id}'").fetchone()

    def get_tokens(self):
        return self.cur.execute(f"SELECT user_token FROM user_token").fetchall()

    def get_tele_token_by_login(self, login):
        tmp = self.cur.execute(f"SELECT tele_token FROM user_token WHERE user_login = '{login}'").fetchone()
        return tmp[0] if tmp is not None else None

    def get_all_boards_by_token(self,token):
        return self.cur.execute(f"SELECT board_id FROM user_boards WHERE user_token='{token}'").fetchall()
