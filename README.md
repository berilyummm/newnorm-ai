# NewNorm AI 🐝 - Modüler Backend Mimarisi

Bu proje, "NewNorm Akıllı Mekan Asistanı" (Nomi) için geliştirilmiş modern, temiz ve tamamen modüler bir Flask backend servisidir. Katmanlı mimari (Layered Architecture) prensiplerine uygun olarak sıfırdan inşa edilmiştir.

## Katmanlı (Modüler) Yapı Açıklaması

Proje kodu aşağıdaki 5 ana modüle bölünmüştür, böylece her dosya sadece kendi işini yapar (Separation of Concerns).

1. **Modül A: Yapılandırma (`app/config.py`)**
   - Sistemin tüm gizli ayarlarını (API anahtarları, veritabanı yolları) merkezi bir yerden yönetir ve `.env` dosyasından okur.

2. **Modül B: Veritabanı Katmanı (`app/database.py`)**
   - Sadece müşteri adayı (Lead) verilerini tutmak ve listelemekle sorumludur. SQLite altyapısı kurulmuştur. SQL sorguları tamamen bu modülün içine hapsedilmiş, dışarı sızması engellenmiştir.

3. **Modül C: Yapay Zeka Servisi (`app/ai_service.py`)**
   - Tamamen izole edilmiş bir servis katmanıdır. Kullanıcı mesajlarını alır, Nomi'nin kimlik bağlamı (Business Context) ile birleştirerek Groq LLM API'sine gönderir ve akıllı yanıtlar döndürür.

4. **Modül D: API ve Rotalar (`app/routes.py`)**
   - Frontend'den (Wix'ten) gelen istekleri HTTP GET/POST olarak karşılayan kontrolcü (Controller) yapısıdır.
   - Gelen verileri doğrular ve işi Modül B (Veritabanı) veya Modül C'ye (Yapay Zeka) delege eder.

5. **Modül E: Fabrika ve Başlatıcı (`app/__init__.py` & `run.py`)**
   - Uygulamayı bir araya getiren (Factory Pattern) ve sunucuyu çalıştıran tetikleyici dosyalardır.

## Frontend (Modül G) & Canlı Kurulum (Modül H) Bağlantıları
- **Wix Sitesi:** [NewNorm AI Canlı Wix Sitesi](https://busraberilciftci.wixstudio.com/wearenewnorm)
- **Canlı Backend Servisi (Render):** [https://newnorm-ai.onrender.com](https://newnorm-ai.onrender.com)
- Wix tarafındaki Velo kodları veya şeffaf buton hot-spotları direkt olarak bu Render adresindeki `/api/chat` ve `/api/leads` endpoint'lerine bağlanmaktadır.

### Kurulum (Geliştiriciler İçin)
```bash
pip install -r requirements.txt
# .env dosyasındaki GROQ_API_KEY değerini girin
python run.py
```
Sunucu `http://localhost:5000` adresinde çalışacaktır.
