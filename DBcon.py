import psycopg2


class DataConnect:
    def __init__(self, db_url):
        self.conn = psycopg2.connect(db_url, sslmode='require')
        self.cur = self.conn.cursor()

    def poom(self, p_name, uou, nk, lk, ku):
        self.cur.execute("SET TIME ZONE 'Asia/Bangkok';")
        self.cur.execute(
            "INSERT INTO p_names (uou, nk, lk, ku, tx) VALUES (%(uou)s, %(nk)s, %(lk)s, %(ku)s, NOW());".replace(
                "p_names",
                p_name),
            {'uou': uou, 'nk': nk, 'lk': lk, 'ku': ku})
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def inputmes(self, sender, receiver, passage, text, time_ln, ans_state):
        self.cur.execute("SET TIME ZONE 'Asia/Bangkok';")

        self.cur.execute(
            "INSERT INTO inputmes (sender, receiver, type, word, time_ln, time_pql, ans_state) VALUES (%(sender)s, "
            "%(receiver)s, %(type)s, %(word)s, %(time_ln)s, NOW(), %(ans_state)s);",
            {'sender': sender, 'receiver': receiver, 'type': passage, 'word': text, 'time_ln': time_ln,
             'ans_state': ans_state})
        self.conn.commit()

        self.cur.close()
        self.conn.close()

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
        self.cur.close()
        self.conn.close()
        return m

    def friends(self, user_id, display_name, status_message):
        self.cur.execute("INSERT INTO friends (user_id, display_name, status_message, time) VALUES (%(user_id)s, "
                    "%(display_name)s, %(status_message)s, NOW());",
                    {'user_id': user_id, 'display_name': display_name, 'status_message': status_message})
        self.conn.commit()

        self.cur.close()
        self.conn.close()

    def answered_text(self, looked, ts):
        self.cur.execute("UPDATE inputmes "
                    "SET ans_state = %(looked)s "
                    "WHERE time_pql = %(int)s;", {'looked': looked, 'int': ts})
        self.conn.commit()

        self.cur.close()
        self.conn.close()

    def word_type(self):
        self.cur.execute("SELECT * "
                    "FROM word_data;")
        m = self.cur.fetchall()
        self.conn.commit()
        self.cur.close()
        self.conn.close()
        return m
