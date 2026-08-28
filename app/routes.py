from flask import Blueprint, jsonify, request, render_template
from . import database

api_bp = Blueprint('api', __name__)
pages_bp = Blueprint('pages', __name__)

@pages_bp.route('/')
def index():
    return render_template('index.html')

@pages_bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@api_bp.route('/leads', methods=['POST', 'OPTIONS'])
def lead_ekle():
    if request.method == 'OPTIONS':
        return '', 200
    veri = request.get_json()
    isim = veri.get('isim', '')
    if veri.get('soyisim'):
        isim += ' ' + veri.get('soyisim')
    telefon = veri.get('telefon', '')
    mesaj = veri.get('mesaj', '')
    if not isim or not telefon or not mesaj:
        return jsonify({"basari": False, "hata": "İsim, telefon ve mesaj zorunludur"}), 400
    database.lead_ekle(isim, telefon, mesaj)
    return jsonify({"basari": True})

@api_bp.route('/leads', methods=['GET', 'OPTIONS'])
def lead_listele():
    if request.method == 'OPTIONS':
        return '', 200
    leads = database.tum_leadler()
    return jsonify({"basari": True, "leads": leads})

@api_bp.route('/leads/<int:lead_id>/durum', methods=['PUT', 'OPTIONS'])
def durum_guncelle_api(lead_id):
    if request.method == 'OPTIONS':
        return '', 200
    veri = request.get_json()
    yeni_durum = veri.get('durum')
    database.durum_guncelle(lead_id, yeni_durum)
    return jsonify({"basari": True})

@api_bp.route('/leads/<int:lead_id>', methods=['DELETE', 'OPTIONS'])
def lead_sil_api(lead_id):
    if request.method == 'OPTIONS':
        return '', 200
    database.lead_sil(lead_id)
    return jsonify({"basari": True})

# app/routes.py dosyasının en altına eklenecek kısım:

import random # (Geçici yapay zeka cevapları için)

@api_bp.route('/sohbet', methods=['POST', 'OPTIONS'])
def sohbet_api():
    if request.method == 'OPTIONS':
        return '', 200
        
    veri = request.get_json()
    kullanici_mesaji = veri.get('mesaj', '')
    gecmis = veri.get('gecmis', [])
    
    # ---------------------------------------------------------
    # BURASI NOMI'NIN BEYNİDİR (İleride buraya OpenAI, Gemini vb. 
    # gerçek bir yapay zeka API'si entegre edeceğiz.)
    # Şimdilik sistemin çalıştığını test etmek için kural tabanlı cevaplar veriyoruz:
    # ---------------------------------------------------------
    
    kullanici_mesaji_kucuk = kullanici_mesaji.lower()
    
    if "fiyat" in kullanici_mesaji_kucuk or "ücret" in kullanici_mesaji_kucuk:
        yanit = "NewNorm'da iç mimarlık hizmetini lüks olmaktan çıkarıyoruz! Odanızın ölçülerine uygun akıllı yerleşim planlarımız bütçe dostu paketlerle sunulmaktadır."
    elif "merhaba" in kullanici_mesaji_kucuk or "selam" in kullanici_mesaji_kucuk:
        yanit = "Merhaba! Ben Nomi. Size küçük alanlarda nasıl daha ferah yaşayabileceğiniz konusunda rehberlik edebilirim. Odanız kaç metrekare?"
    elif "küçük" in kullanici_mesaji_kucuk or "dar" in kullanici_mesaji_kucuk:
        yanit = "Küçük alanlarda yaşamak bir mahrumiyet değildir! Size özel katlanabilir mobilya ve akıllı saklama çözümleri önerebilirim."
    else:
        # Rastgele genel cevaplar
        genel_cevaplar = [
            "Bu harika bir soru! Akıllı yaşam felsefemiz tam da bu konulara odaklanıyor.",
            "Anlıyorum. Dar alanlardaki psikolojik ferahlığı artırmak için açık renkler ve modüler eşyalar tavsiye ediyoruz.",
            "Bunu biraz daha detaylandırabilir misiniz? Size en uygun akıllı mobilyayı bulmak isterim."
        ]
        yanit = random.choice(genel_cevaplar)
        
    # Yanıtı Wix'in anlayacağı şekilde (JSON formatında) Frontend'e geri gönderiyoruz
    return jsonify({"basari": True, "yanit": yanit})
