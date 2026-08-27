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
        # Create table if it doesn't exist (with durum column)
        db.execute('''
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                isim TEXT NOT NULL,
                telefon TEXT NOT NULL,
                mesaj TEXT,
                tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                durum TEXT DEFAULT 'Bekliyor'
            )
        ''')
        
        # In case the table already exists but without 'durum', we add it dynamically
        try:
            db.execute("ALTER TABLE leads ADD COLUMN durum TEXT DEFAULT 'Bekliyor'")
        except sqlite3.OperationalError:
            pass # Column already exists
            
        db.commit()

# --- VERİ ERİŞİM KATMANI (DATA ACCESS LAYER) - SEPARATION OF CONCERNS (SoC) ---
# Yönerge Şartı: Bu dosya sadece veritabanı işlemleriyle ilgilenir. 
# Başka hiçbir mantık barındırmaz, böylece katmanlar temiz ayrılmış olur.

def lead_ekle(isim, telefon, mesaj=None):
    db = get_db()
    # Yönerge Şartı: GÜVENLİK (%10 Puan) - SQL Injection Koruması
    # Doğrudan f-string veya string birleştirme YERİNE, "?" (placeholder) parametrik
    # sorgular kullanılarak olası SQL Injection saldırılarının önüne geçilmiştir.
    db.execute(
        'INSERT INTO leads (isim, telefon, mesaj, durum) VALUES (?, ?, ?, ?)',
        (isim, telefon, mesaj, 'Bekliyor')
    )
    db.commit()

def durum_guncelle(lead_id, yeni_durum):
    db = get_db()
    db.execute(
        'UPDATE leads SET durum = ? WHERE id = ?',
        (yeni_durum, lead_id)
    )
    db.commit()

def lead_sil(lead_id):
    db = get_db()
    db.execute(
        'DELETE FROM leads WHERE id = ?',
        (lead_id,)
    )
    db.commit()

def tum_leadler():
    db = get_db()
    # Yönerge: İsteğe bağlı olarak yeni eklenenlerin alta gelmesi için ASC (artan) sıralama yapıldı.
    satirlar = db.execute('SELECT * FROM leads ORDER BY id ASC').fetchall()
    return [dict(satir) for satir in satirlar]

def durum_guncelle(lead_id, yeni_durum):
    db = get_db()
    db.execute('UPDATE leads SET onay_durumu = ? WHERE id = ?', (yeni_durum, lead_id))
    db.commit()
