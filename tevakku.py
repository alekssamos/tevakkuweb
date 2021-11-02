import sqlite3
import os
import os.path

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class Tevakku():
    "search in DB"
    def __init__(self, filename:str = "tevakku.db"):
        if not os.path.isfile(filename):
            raise ValueError("DB file not found")
        self.filename = filename

    def sentences(self, q:str)->dict:
        with sqlite3.connect(self.filename) as conn:
            conn.row_factory = dict_factory
            cur = conn.cursor()
            cur.execute("SELECT * FROM sentences WHERE sentence like '%'||?||'%' OR translation like '%'||?||'%'", (q,q))
            return cur.fetchall()

    def tevakku_fts(self, q:str):
        with sqlite3.connect(self.filename) as conn:
            conn.row_factory = dict_factory
            cur = conn.cursor()
            cur.execute("SELECT * FROM tevakku_fts WHERE word_search like '%'||?||'%' OR word like '%'||?||'%'  OR meanings_strong like '%'||?||'%' OR meanings_weak like '%'||?||'%' OR description like '%'||?||'%' OR description_search like '%'||?||'%'", (q,q,q,q,q,q))
            return cur.fetchall()

    def tevakku(self, q:str):
        with sqlite3.connect(self.filename) as conn:
            conn.row_factory = dict_factory
            cur = conn.cursor()
            cur.execute("SELECT * FROM tevakku WHERE word_search = '?' OR word = '?' OR description_search like '%'||?||'%'", (q,q,q))
            return cur.fetchall()
