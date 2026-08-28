import os
import google.generativeai as genai
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
# NOMI AI (GERÇEK YAPAY ZEKA) BAĞLANTISI
# ========================================================

@api_bp.route('/sohbet', methods=['POST', 'OPTIONS'])
def sohbet_api():
    if request.method == 'OPTIONS':
        return '', 200
        
    veri = request.get_json()
    kullanici_mesaji = veri.get('mesaj', '')
    
    # 1. Render'daki "Environment Variables" kısmına eklediğimiz şifreyi alıyoruz
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return jsonify({"basari": True, "yanit": "Sistem hatası: Yapay zeka API anahtarı Render'da bulunamadı! Lütfen ayarlarınızı kontrol edin."})
        
    # 2. Yapay zekayı bu şifreyle yetkilendiriyoruz
    genai.configure(api_key=api_key)
    
    # 3. Nomi'nin Kişiliği ve Şirket Kuralları (Sistem İstemi)
    sistem_talimati = """
    Senin adın Nomi. Sen 'NewNorm' şirketinin resmi yapay zeka asistanısın.
    Amacın: Büyük şehirlerde küçük evlerde (1+1, 1+0 vb.) yaşayan insanlara akıllı yaşam tarzı, bütçe dostu modüler mobilya dizilimi ve psikolojik olarak ferah hissettirecek dekorasyon tavsiyeleri vermektir.
    Kullanıcılara pahalı iç mimarlık hizmetleri yerine zekice ve ekonomik çözümler (örneğin katlanabilir yataklar, çok amaçlı dolaplar, aynalarla derinlik algısı vb.) sunarsın.
    Her zaman samimi, profesyonel, anlayışlı ve empatik bir dil kullan. Asla başka bir yapay zeka modelinden veya Google'dan bahsetme, sadece "NewNorm Asistanı Nomi" olarak konuş. 
    Cevaplarını her zaman olabildiğince kısa, net ve okunması kolay (1-2 paragraf) tut.
    """
    
    # 4. Hızlı ve Zeki Gemini 1.5 Flash Modelini Ayarlama
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=sistem_talimati
    )
    
    try:
        # Nomi mesajı okur ve üretir
        response = model.generate_content(kullanici_mesaji)
        yanit = response.text
        
        # Sonucu Wix'e geri yolluyoruz
        return jsonify({"basari": True, "yanit": yanit})
        
    except Exception as e:
        print("Nomi AI Hatası:", str(e))
        return jsonify({"basari": False, "hata": "Nomi şu an düşünüyor ama cevap veremedi."}), 500
