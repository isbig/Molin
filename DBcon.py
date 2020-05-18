import psycopg2
import config
import os

DATABASE_URL = os.getenv('DATABASE_URL')
# DATABASE_URL = config.DATABASE_URL
conn = psycopg2.connect(DATABASE_URL, sslmode='require')

cur = conn.cursor()
cur.execute("SELECT * "
            "FROM word_data;")
m = cur.fetchall()


def poom(p_name, uou, nk, lk, ku):
    cur.execute("SET TIME ZONE 'Asia/Bangkok';")
    cur.execute(
        "INSERT INTO p_names (uou, nk, lk, ku, tx) VALUES (%(uou)s, %(nk)s, %(lk)s, %(ku)s, NOW());".replace("p_names",
                                                                                                             p_name),
        {'uou': uou, 'nk': nk, 'lk': lk, 'ku': ku})
    conn.commit()
    cur.close()
    conn.close()


def inputmes(sender, receiver, passage, text, time_ln, ans_state):
    cur.execute("SET TIME ZONE 'Asia/Bangkok';")

    cur.execute("INSERT INTO inputmes (sender, receiver, type, word, time_ln, time_pql, ans_state) VALUES (%(sender)s, "
                "%(receiver)s, %(type)s, %(word)s, %(time_ln)s, NOW(), %(ans_state)s);",
                {'sender': sender, 'receiver': receiver, 'type': passage, 'word': text, 'time_ln': time_ln,
                 'ans_state': ans_state})
    conn.commit()

    cur.close()
    conn.close()


def find_mess(sender, receiver, back, bon):
    # from https://stackoverflow.com/questions/6267887/get-last-record-of-a-table-in-postgres
    if bon == 1:
        cur.execute("SELECT * "
                    "FROM inputmes "
                    "WHERE sender = %(sender)s AND receiver = %(receiver)s"
                    "ORDER BY time_ln DESC LIMIT %(back)s;", {'sender': sender, 'receiver': receiver, 'back': back})
    elif bon == 2:
        cur.execute("SELECT * "
                    "FROM inputmes "
                    "WHERE (sender = %(sender)s AND receiver = %(receiver)s) OR (sender = %(receiver)s AND receiver = %(sender)s)"
                    "ORDER BY time_ln DESC LIMIT %(back)s;", {'sender': sender, 'receiver': receiver, 'back': back})
    m = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return m


def friends(user_id, display_name, status_message):
    cur.execute("INSERT INTO friends (user_id, display_name, status_message, time) VALUES (%(user_id)s, "
                "%(display_name)s, %(status_message)s, NOW());",
                {'user_id': user_id, 'display_name': display_name, 'status_message': status_message})
    conn.commit()

    cur.close()
    conn.close()


def answered_text(looked, ts):
    cur.execute("UPDATE inputmes "
                "SET ans_state = %(looked)s "
                "WHERE time_pql = %(int)s;", {'looked': looked, 'int': ts})
    conn.commit()

    cur.close()
    conn.close()


def word_type():
    cur.execute("SELECT * "
                "FROM word_data;")
    m = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return m