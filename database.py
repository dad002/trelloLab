import sqlite3

class DataBase:

    def __init__(self):
        self.con = sqlite3.connect('data.db', check_same_thread=False)
        self.cur = self.con.cursor()


    def create_tables(self):

        self.cur.execute("""CREATE TABLE IF NOT EXISTS user_token (tele_token TEXT, user_token TEXT)""")
        self.cur.execute("""CREATE TABLE IF NOT EXISTS user_boards (user_token TEXT, board_id TEXT)""")
        self.cur.execute("""CREATE TABLE IF NOT EXISTS board_info (board_id TEXT, message_type INTEGER)""")


    def set_user_token_data(self, data):

        self.cur.execute(f"""INSERT INTO user_token (tele_token, user_token) 
            SELECT '{data[0]}', '{data[1]}' 
            WHERE NOT EXISTS 
            (SELECT 1 FROM user_token WHERE tele_token='{data[0]}' AND user_token='{data[1]}')""")
        self.con.commit()

    def set_user_board_data(self, data):

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
        return self.cur.execute(f"""SELECT user_token FROM user_token WHERE tele_token='{token}'""").fetchone()[0]