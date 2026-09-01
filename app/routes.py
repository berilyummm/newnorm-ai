import os
import requests
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


# ========================================================
# NOMI AI - GROQ (LLAMA 3) BAĞLANTISI
# ========================================================

@api_bp.route('/sohbet', methods=['POST', 'OPTIONS'])
def sohbet_api():
    if request.method == 'OPTIONS':
        return '', 200
        
    veri = request.get_json()
    kullanici_mesaji = veri.get('mesaj', '')
    
    # 1. Render'daki GROQ_API_KEY şifresini alıyoruz 
    # (Eğer ismini değiştirmediyseniz diye GEMINI_API_KEY'i de kontrol ediyoruz)
    api_key = os.environ.get("GROQ_API_KEY") or os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return jsonify({"basari": True, "yanit": "Sistem hatası: GROQ API anahtarı Render'da bulunamadı!"})
        
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # 2. Nomi'nin Kişiliği ve Şirket Kuralları (Sistem İstemi)
    sistem_talimati = """
    Senin adın Nomi. Sen 'NewNorm' şirketinin resmi yapay zeka asistanısın.
    Amacın: Büyük şehirlerde küçük evlerde yaşayan insanlara akıllı yaşam tarzı ve ferahlatıcı dekorasyon tavsiyeleri vermektir.
    Kullanıcılara zekice ve bütçe dostu çözümler sunarsın.
    
    ÖNEMLİ KURAL: Kullanıcı seninle hangi dilde yazışıyorsa, ona KESİNLİKLE o dilde cevap vermelisin (İngilizce sorarsa İngilizce, Almanca sorarsa Almanca vb.).
    
    KESİN KURAL: Cevaplarını her zaman KESİNLİKLE çok kısa, net ve en fazla 1-2 cümle olarak vermelisin. Asla uzun listeler veya paragraflar yazma. Samimi ve nokta atışı konuş.
    """
    
    # 3. Groq üzerinden süper hızlı Llama 3 modelini çağırıyoruz
    data = {
        "model": "openai/gpt-oss-120b", 
        "messages": [
            {"role": "system", "content": sistem_talimati},
            {"role": "user", "content": kullanici_mesaji}
        ],
        "temperature": 0.7
    }
    
    try:
        # Nomi mesajı Groq'a gönderir ve cevabı alır
        response = requests.post(url, headers=headers, json=data)
        response_json = response.json()
        
        # Eğer API şifresi hatalıysa veya Groq'tan hata gelirse bunu göster
        if "error" in response_json:
            return jsonify({"basari": True, "yanit": f"Groq Hatası: {response_json['error']['message']}"})
            
        yanit = response_json['choices'][0]['message']['content']
        
        # Sonucu Wix'e geri yolluyoruz
        return jsonify({"basari": True, "yanit": yanit})
        
    except Exception as e:
        hata_mesaji = f"Sistem Hatası Detayı: {str(e)}"
        return jsonify({"basari": True, "yanit": hata_mesaji})


