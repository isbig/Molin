import psycopg2


class DataConnect:
    def __init__(self, db_url):
        self.db_url = db_url
        self.conn = psycopg2.connect(db_url, sslmode='require')
        self.cur = self.conn.cursor()

    def poom(self, poom_num, uou, nk, lk, ku):
        self.cur.execute("SET TIME ZONE 'Asia/Bangkok';")
        self.cur.execute(
            "INSERT INTO poom (uou, nk, lk, ku, tx, poom_num) VALUES (%(uou)s, %(nk)s, %(lk)s, %(ku)s, NOW(), "
            "%(poom)s);", {'uou': uou, 'nk': nk, 'lk': lk, 'ku': ku, 'poom': poom_num})
        self.conn.commit()

    def inputmes(self, sender, receiver, passage, text, time_ln, ans_state):
        self.cur.execute("SET TIME ZONE 'Asia/Bangkok';")

        self.cur.execute(
            "INSERT INTO inputmes (sender, receiver, type, word, time_ln, time_pql, ans_state) VALUES (%(sender)s, "
            "%(receiver)s, %(type)s, %(word)s, %(time_ln)s, NOW(), %(ans_state)s);",
            {'sender': sender, 'receiver': receiver, 'type': passage, 'word': text, 'time_ln': time_ln,
             'ans_state': ans_state})
        self.conn.commit()

    def find_mess(self, sender, receiver, back, bon):
        # from https://stackoverflow.com/questions/6267887/get-last-record-of-a-table-in-postgres
        if bon == 1:
            self.cur.execute("SELECT * "
                        "FROM inputmes "
                        "WHERE sender = %(sender)s AND receiver = %(receiver)s"
                        "ORDER BY time_ln DESC LIMIT %(back)s;", {'sender': sender, 'receiver': receiver, 'back': back})
        elif bon == 2:
            self.cur.execute("SELECT * "
                        "FROM inputmes "
                        "WHERE (sender = %(sender)s AND receiver = %(receiver)s) OR (sender = %(receiver)s AND receiver = %(sender)s)"
                        "ORDER BY time_ln DESC LIMIT %(back)s;", {'sender': sender, 'receiver': receiver, 'back': back})
        m = self.cur.fetchall()
        self.conn.commit()
        return m

    def friends(self, user_id, display_name, status_message):
        self.cur.execute("INSERT INTO friends (user_id, display_name, status_message, time) VALUES (%(user_id)s, "
                    "%(display_name)s, %(status_message)s, NOW());",
                    {'user_id': user_id, 'display_name': display_name, 'status_message': status_message})
        self.conn.commit()

    def answered_text(self, looked, ts):
        self.cur.execute("UPDATE inputmes "
                    "SET ans_state = %(looked)s "
                    "WHERE time_pql = %(int)s;", {'looked': looked, 'int': ts})
        self.conn.commit()

    def word_type(self):
        self.cur.execute("SELECT * "
                    "FROM word_data;")
        m = self.cur.fetchall()
        self.conn.commit()
        return m

    def close_con(self):
        self.cur.close()
        self.conn.close()


class FinePum:
    def __init__(self, db_url):
        self.conn = psycopg2.connect(db_url, sslmode='require')
        self.cur = self.conn.cursor()

    # หาหน่วยย่อยล่าสุดที่เกี่ยวกับสิ่ง ๆ หนึ่ง
    def find_last_ks(self, fw):
        # from https://stackoverflow.com/questions/6267887/get-last-record-of-a-table-in-postgres
        self.cur.execute("SELECT * "
                         "FROM poom "
                         "WHERE nk = %(fw)s or lk = %(fw)s "
                         "ORDER BY tx DESC LIMIT %(back)s;", {'fw': fw, 'back': 1})
        m = self.cur.fetchall()
        self.conn.commit()
        return m

    # หากรอบล่าสุดที่เกี่ยวกับสิ่ง ๆ หนึ่ง
    def find_ks_name(self, fw):
        a = self.find_last_ks(fw)
        a1, a2, a3, a4, a5, a6 = a[0]
        return a4

    # หาหน่วยย่อยโดยใช้กรอบ จะได้หน่วยย่อยทั้งหมดที่มีกรอบเดียวกัน
    def find_pum(self, ks):
        self.cur.execute("SELECT * "
                         "FROM poom "
                         "WHERE ku = %(ku)s;", {'ku': ks})
        m = self.cur.fetchall()
        self.conn.commit()
        return m

    # หาหน่วยย่อยทั้งหมดในกรอบล่าสุดที่เกี่ยวกับสิ่ง ๆ หนึ่ง หรือคน ๆ หนึ่ง
    def last_ks(self, who):
        return self.find_pum(self.find_ks_name(who))

    def close_con(self):
        self.cur.close()
        self.conn.close()
