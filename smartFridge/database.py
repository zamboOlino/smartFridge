import sqlite3


class Database:
    def __init__(self, db="database‚"):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS article (
                id      INTEGER PRIMARY KEY AUTOINCREMENT, 
                ean     TEXT, 
                article TEXT,
                note    TRXT, 
                mhd     TEXT)""")
        self.conn.commit()

    def find_by_ean(self, ean = ''):
        self.cur.execute(f"SELECT * FROM article WHERE ean = '{ean}'")
        rows = self.cur.fetchall()
        return rows

    def find_by_article(self, article = ''):
        self.cur.execute(f"SELECT * FROM article WHERE article = '{article}'")
        rows = self.cur.fetchall()
        return rows

    def find_all(self, query = "SELECT * FROM article"):
        self.cur.execute(query)
        rows = self.cur.fetchall()
        return rows

    def insert(self, ean, article, note, mhd):
        self.cur.execute(f"INSERT INTO article (ean, article, note, mhd) VALUES ('{ean}', '{article}', '{note}', '{mhd}')")
        self.conn.commit()

    def remove(self, id):
        self.cur.execute(f"DELETE FROM article WHERE id={id}")
        self.conn.commit()

    def update(self, id, ean, article, note, mhd):
        self.cur.execute(f"UPDATE article SET ean = '{ean}', article = '{article}', note = '{note}', mhd = '{mhd}' WHERE id = {id}")
        self.conn.commit()

    def __del__(self):
        self.conn.close()

if __name__ == '__main__':
    db = Database()

    db.insert('4337185552175', 'Testartikel', "", "20220510")

    for record in db.find_all():
        print(record)
        db.remove(record[0])

    del db

