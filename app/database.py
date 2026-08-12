import sqlite3
from flask import g, current_app

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE_URL'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db(app):
    with app.app_context():
        db = get_db()
        # Yonergere tam uyumlu, basit yapi (extra kolonlar silindi)
        db.execute('''
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                isim TEXT NOT NULL,
                telefon TEXT NOT NULL,
                mesaj TEXT,
                tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        db.commit()

def lead_ekle(isim, telefon, mesaj=None):
    db = get_db()
    # SQL Injection'a karsi ? (soru isareti) ile koruma (Yonerge zorunlulugu)
    db.execute(
        'INSERT INTO leads (isim, telefon, mesaj) VALUES (?, ?, ?)',
        (isim, telefon, mesaj)
    )
    db.commit()

def tum_leadler():
    db = get_db()
    # En yeniden en eskiye dogru (Yonerge sarti)
    satirlar = db.execute('SELECT * FROM leads ORDER BY tarih DESC').fetchall()
    return [dict(satir) for satir in satirlar]
