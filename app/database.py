import sqlite3
import datetime
from .config import Config

def get_db():
    """Veritabanına bağlanır; satırlara sütun adıyla erişim sağlar."""
    conn = sqlite3.connect(Config.DATABASE_URL)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(app):
    """'leads' tablosunu genişletilmiş alanlarla oluşturur (yoksa)."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            isim TEXT NOT NULL,
            soyisim TEXT,
            eposta TEXT,
            alan_kodu TEXT,
            telefon TEXT NOT NULL,
            butce TEXT,
            aciklama TEXT,
            mesaj TEXT,
            durum TEXT DEFAULT 'bekliyor',
            tarih TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def lead_ekle(isim, soyisim, eposta, alan_kodu, telefon, butce, aciklama, mesaj=None):
    """Genişletilmiş alanlarla yeni kayıt ekler. SQL Injection korumalı."""
    tarih = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    durum = "bekliyor" # Varsayılan durum
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO leads (isim, soyisim, eposta, alan_kodu, telefon, butce, aciklama, mesaj, durum, tarih)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (isim, soyisim, eposta, alan_kodu, telefon, butce, aciklama, mesaj, durum, tarih))
    
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
    
    return [dict(row) for row in rows]

def lead_durum_guncelle(lead_id, yeni_durum):
    """Bir lead'in durumunu günceller (onaylandi, reddedildi, bekliyor)."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE leads SET durum = ? WHERE id = ?
    ''', (yeni_durum, lead_id))
    
    # Etkilenen satır sayısını kontrol et
    rowcount = cursor.rowcount
    conn.commit()
    conn.close()
    
    if rowcount == 0:
        raise ValueError("Kayıt bulunamadı.")
    return True

def lead_sil(lead_id):
    """Bir lead'i veritabanından kalıcı olarak siler."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM leads WHERE id = ?', (lead_id,))
    rowcount = cursor.rowcount
    conn.commit()
    conn.close()
    
    if rowcount == 0:
        raise ValueError("Kayıt bulunamadı.")
    return True
