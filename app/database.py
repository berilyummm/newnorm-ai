import sqlite3
import datetime
from .config import Config

def get_db():
    """Veritabanına bağlanır; satırlara sütun adıyla erişim sağlar."""
    conn = sqlite3.connect(Config.DATABASE_URL)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(app):
    """'leads' tablosunu oluşturur (yoksa)."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            isim TEXT NOT NULL,
            telefon TEXT NOT NULL,
            mesaj TEXT,
            tarih TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def lead_ekle(isim, telefon, mesaj=None):
    """Yeni kayıt ekler. SQL Injection'a karşı ? yer tutucusu kullanır."""
    tarih = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = get_db()
    cursor = conn.cursor()
    
    # ? yer tutucuları ve parametreler ile güvenli ekleme işlemi
    cursor.execute('''
        INSERT INTO leads (isim, telefon, mesaj, tarih)
        VALUES (?, ?, ?, ?)
    ''', (isim, telefon, mesaj, tarih))
    
    conn.commit()
    conn.close()
    return True

def tum_leadler():
    """Tüm kayıtları en yeniden eskiye getirir."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM leads ORDER BY id DESC')
    rows = cursor.fetchall()
    conn.close()
    
    # sqlite3.Row objelerini JSON serileştirilebilir sözlüklere (dict) çevirme
    return [dict(row) for row in rows]
