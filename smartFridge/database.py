import sqlite3


class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS article (
                id      INTEGER PRIMARY KEY, 
                ean     TEXT, 
                article TEXT, 
                mhd     TEXT)""")
        self.conn.commit()

    def find_by_ean(self, ean=''):
        self.cur.execute(f"SELECT * FROM article WHERE ean = {ean}")
        rows = self.cur.fetchall()
        return rows

    def find_all(self, query):
        self.cur.execute(query)
        rows = self.cur.fetchall()
        return rows

    def insert(self, ean, article, mhd):
        self.cur.execute(f"INSERT INTO article VALUES (NULL, {ean}, {article}, {mhd})")
        self.conn.commit()

    def remove(self, id):
        self.cur.execute(f"DELETE FROM article WHERE id={id}")
        self.conn.commit()

    def update(self, id, ean, article, mhd):
        self.cur.execute(f"UPDATE article SET ean = {ean}, article = {article}, mhd = {mhd} WHERE id = {id}")
        self.conn.commit()

    def __del__(self):
        self.conn.close()
