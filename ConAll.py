import psycopg2
import time
import random
import config
import os


def current_milli_time():
    return int(round(time.time() * 1000))


ran_in = random.randint(0, 9)
k_rob = str(current_milli_time())+str(ran_in)


class CreateMainUnit:
    def __init__(self, text, frame):
        self.text = text
        self.frame = str(frame)
        self.kb = k_rob
        try:
            db_url = os.getenv('DATABASE_URL')
            self.conn = psycopg2.connect(db_url, sslmode='require')
        except:
            db_url = config.DATABASE_URL
            self.conn = psycopg2.connect(db_url, sslmode='require')
        self.cur = self.conn.cursor()
        self.input_to_au_ort()

    def regrbo(self):
        return self.kb

    def input_to_au_ort(self):
        self.cur.execute("SET TIME ZONE 'Asia/Bangkok';")
        self.cur.execute(
            "INSERT INTO allunit (original_text, times, grob, grobby, unit_num) VALUES (%(text)s, NOW(), %(frame)s, "
            "%(grobby)s, %(unit_num)s);", {'text': self.text, 'frame': self.frame, 'grobby': self.kb, 'unit_num': '1'})
        self.conn.commit()

    def update_event(self, event):
        self.cur.execute(
            "UPDATE allunit "
            "SET kriya = %(event)s "
            "WHERE grobby = %(grobby)s AND unit_num = %(unit_num)s;",
            {'event': event, 'grobby': self.kb, 'unit_num': '1'})
        self.conn.commit()

    def update_namna(self, namna):
        self.cur.execute(
            "UPDATE allunit "
            "SET namna = %(namna)s "
            "WHERE grobby = %(grobby)s AND unit_num = %(unit_num)s;",
            {'namna': namna, 'grobby': self.kb, 'unit_num': '1'})
        self.conn.commit()

    def update_namlang(self, namlang):
        self.cur.execute(
            "UPDATE allunit "
            "SET namlang = %(namlang)s "
            "WHERE grobby = %(grobby)s AND unit_num = %(unit_num)s;",
            {'namlang': namlang, 'grobby': self.kb, 'unit_num': '1'})
        self.conn.commit()

    def update_namperm(self, namperm):
        self.cur.execute(
            "UPDATE allunit "
            "SET namperm = %(namperm)s "
            "WHERE grobby = %(grobby)s AND unit_num = %(unit_num)s;",
            {'namperm': namperm, 'grobby': self.kb, 'unit_num': '1'})
        self.conn.commit()

    def update_backk(self, backk):
        self.cur.execute(
            "UPDATE allunit "
            "SET backk = %(backk)s "
            "WHERE grobby = %(grobby)s AND unit_num = %(unit_num)s;",
            {'backk': backk, 'grobby': self.kb, 'unit_num': '1'})
        self.conn.commit()

    def update_frontk(self, frontk):
        self.cur.execute(
            "UPDATE allunit "
            "SET frontk = %(frontk)s "
            "WHERE grobby = %(grobby)s AND unit_num = %(unit_num)s;",
            {'frontk': frontk, 'grobby': self.kb, 'unit_num': '1'})
        self.conn.commit()

    def close_con(self):
        self.cur.close()
        self.conn.close()


# add unit to grobby
class AddUnit:
    def __init__(self, text, grobby):
        self.text = text
        self.grobby = grobby
        k = FineObject(grobby)
        self.n = str(k.find_grobby_unit_num()+1)  # unit num
        try:
            db_url = os.getenv('DATABASE_URL')
            self.conn = psycopg2.connect(db_url, sslmode='require')
        except:
            db_url = config.DATABASE_URL
            self.conn = psycopg2.connect(db_url, sslmode='require')
        self.cur = self.conn.cursor()
        self.add_unit()

    def add_unit(self,):
        self.cur.execute("SET TIME ZONE 'Asia/Bangkok';")
        self.cur.execute(
                "INSERT INTO allunit (original_text, times, grobby, unit_num) VALUES (%(text)s, NOW(), "
                "%(grobby)s, %(unit_num)s);", {'text': self.text, 'grobby': self.grobby, 'unit_num': self.n})
        self.conn.commit()
        return self.n

    def update_grob(self, grob):
        self.cur.execute(
            "UPDATE allunit "
            "SET grob = %(grob)s "
            "WHERE grobby = %(grobby)s AND unit_num = %(unit_num)s;",
            {'grob': grob, 'grobby': self.grobby, 'unit_num': self.n})
        self.conn.commit()

    def update_event(self, event):
        self.cur.execute(
            "UPDATE allunit "
            "SET kriya = %(event)s "
            "WHERE grobby = %(grobby)s AND unit_num = %(unit_num)s;",
            {'event': event, 'grobby': self.grobby, 'unit_num': self.n})
        self.conn.commit()

    def update_namna(self, namna):
        self.cur.execute(
            "UPDATE allunit "
            "SET namna = %(namna)s "
            "WHERE grobby = %(grobby)s AND unit_num = %(unit_num)s;",
            {'namna': namna, 'grobby': self.grobby, 'unit_num': self.n})
        self.conn.commit()

    def update_namlang(self, namlang):
        self.cur.execute(
            "UPDATE allunit "
            "SET namlang = %(namlang)s "
            "WHERE grobby = %(grobby)s AND unit_num = %(unit_num)s;",
            {'namlang': namlang, 'grobby': self.grobby, 'unit_num': self.n})
        self.conn.commit()

    def update_namperm(self, namperm):
        self.cur.execute(
            "UPDATE allunit "
            "SET namperm = %(namperm)s "
            "WHERE grobby = %(grobby)s AND unit_num = %(unit_num)s;",
            {'namperm': namperm, 'grobby': self.grobby, 'unit_num': self.n})
        self.conn.commit()

    def update_backk(self, backk):
        self.cur.execute(
            "UPDATE allunit "
            "SET backk = %(backk)s "
            "WHERE grobby = %(grobby)s AND unit_num = %(unit_num)s;",
            {'backk': backk, 'grobby': self.grobby, 'unit_num': self.n})
        self.conn.commit()

    def update_frontk(self, frontk):
        self.cur.execute(
            "UPDATE allunit "
            "SET frontk = %(frontk)s "
            "WHERE grobby = %(grobby)s AND unit_num = %(unit_num)s;",
            {'frontk': frontk, 'grobby': self.grobby, 'unit_num': self.n})
        self.conn.commit()

    def close_con(self):
        self.cur.close()
        self.conn.close()


class FineObject:
    def __init__(self, grobby):
        self.grobby = grobby
        try:
            db_url = os.getenv('DATABASE_URL')
            self.conn = psycopg2.connect(db_url, sslmode='require')
        except:
            db_url = config.DATABASE_URL
            self.conn = psycopg2.connect(db_url, sslmode='require')
        self.cur = self.conn.cursor()

    # return grobby number หาทำไม
    def find_grobby_detail(self):
        # from https://stackoverflow.com/questions/6267887/get-last-record-of-a-table-in-postgres
        self.cur.execute("SELECT * "
                         "FROM allunit "
                         "WHERE grobby = %(grobby)s "
                         "ORDER BY tx DESC LIMIT %(back)s;", {'grobby': self.grobby, 'back': 1})
        m = self.cur.fetchall()
        self.conn.commit()
        a1, a2, a3, a4, a5, a6, a7, a8, a9, a10 = m[0]
        return a8

    # return number of unit
    def find_grobby_unit_num(self):
        # from https://stackoverflow.com/questions/6267887/get-last-record-of-a-table-in-postgres
        self.cur.execute("SELECT * "
                         "FROM allunit "
                         "WHERE grobby = %(grobby)s;", {'grobby': self.grobby})
        m = self.cur.fetchall()
        self.conn.commit()
        s = len(m)
        return s

    def close_con(self):
        self.cur.close()
        self.conn.close()
