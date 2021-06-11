import sqlite3
from settings import creator_post_skip

class DB:
    def __init__(self):
        self.create_db_comments()
        self.create_db_post()

    def check_post(self, record):
        """
        return boleean
        false- if creator in skiplist or post in bd
        """

        con = sqlite3.connect(f'records.db')
        cur = con.cursor()

        cur.execute(f'''SELECT id_post
                FROM posts
                WHERE id_post = ? ''',
                    (record.get('id_post'),))
        exists = cur.fetchall()

        if not exists:
            if record.get('id_creator') in creator_post_skip:
                cur.execute(f'''INSERT INTO posts  VALUES (? ,? )''',
                            (record.get('id_post'), record.get('id_creator')))
                con.commit()
                con.close()
                return False
            else:

                cur.execute(f'''INSERT INTO posts  VALUES (? ,? )''',
                            (record.get('id_post'), record.get('id_creator')))
                con.commit()
                con.close()

                return True
        else:

            con.commit()
            con.close()
            return False
    def check_comments(self, record):
        con = sqlite3.connect(f'records.db')
        cur = con.cursor()


        cur.execute(f'''SELECT id_post, id_comment, podcommentid 
        FROM comments 
        WHERE id_post = ? AND id_comment = ? AND podcommentid= ? ''',
                    (record[0], record[1], record[2]))
        exists = cur.fetchall()

        if not exists:
            if record[3] != 0:
                cur.execute(f'''INSERT INTO comments  VALUES (? ,? ,? , ?)''',
                            (record[0], record[1], record[2], record[3]))
                con.commit()
                con.close()
                return False
            else:

                cur.execute(f'''INSERT INTO comments  VALUES (? ,? ,? , ?)''',
                            (record[0], record[1], record[2], record[3]))
                con.commit()
                con.close()

                return True
        else:

            con.commit()
            con.close()
            return False

    def update_bd_comments(self,record):
        con = sqlite3.connect(f'records.db')
        cur = con.cursor()
        cur.execute(
            '''UPDATE comments SET is_admin = 1 
        WHERE id_post = ? 
        AND podcommentid =? 
        AND id_comment = ?;''', (record[0], record[1], record[2]))
        con.commit()
        con.close()

    def create_db_comments(self):
        con = sqlite3.connect(f'records.db')
        cur = con.cursor()

        cur.execute(f'''CREATE TABLE IF NOT EXISTS comments(
           id_post TEXT ,
           id_comment TEXT,
           podcommentid TEXT,
           is_admin INT)''')

        con.commit()
        con.close()
    def create_db_post(self):
        con = sqlite3.connect(f'records.db')
        cur = con.cursor()

        cur.execute(f'''CREATE TABLE IF NOT EXISTS posts(
           id_post TEXT ,
           id_creator TEXT )''')

        con.commit()
        con.close()


