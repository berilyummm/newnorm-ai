from flask import Blueprint, jsonify, request, render_template, redirect, url_for
from .services.ai_service import ai_service, AIServiceError
from . import database

api_bp = Blueprint('api', __name__)
pages_bp = Blueprint('pages', __name__)

# ==========================================
# 1. HTML SAYFALARI (ŞİFRESİZ DASHBOARD)
# ==========================================
@pages_bp.route('/')
def index():
    return render_template('index.html')

@pages_bp.route('/chat')
def chat():
    return render_template('chat.html')

@pages_bp.route('/dashboard')
def dashboard():
    # DİKKAT: Şifre (login) kontrolü tamamen KALDIRILDI. Direkt açılacak.
    return render_template('dashboard.html')


# ==========================================
# 2. WIX İÇİN API UÇ NOKTALARI
# ==========================================
@api_bp.route('/sohbet', methods=['POST', 'OPTIONS'])
def sohbet():
    if request.method == 'OPTIONS':
        return '', 200
    veri = request.get_json()
    if not veri or 'mesaj' not in veri:
        return jsonify({"basari": False, "hata": "Mesaj gerekli"}), 400
        
    mesaj = veri['mesaj']
    gecmis = veri.get('gecmis', [])
    
    try:
        yanit = ai_service.yanit_uret(mesaj, gecmis)
        return jsonify({"basari": True, "yanit": yanit})
    except AIServiceError as e:
        return jsonify({"basari": False, "hata": str(e)}), 503

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
    return jsonify({"basari": True, "mesaj": "Kayıt başarıyla eklendi"}), 201

@api_bp.route('/leads', methods=['GET', 'OPTIONS'])
def lead_listele():
    if request.method == 'OPTIONS':
        return '', 200
        
    leads = database.tum_leadler()
    return jsonify({"basari": True, "leads": leads})

@api_bp.route('/istatistikler', methods=['GET', 'OPTIONS'])
def istatistikler():
    if request.method == 'OPTIONS':
        return '', 200
        
    stats = database.istatistikleri_getir()
    stats["basari"] = True
    return jsonify(stats)

@api_bp.route('/leads/<int:lead_id>/durum', methods=['PUT', 'OPTIONS'])
def durum_guncelle_api(lead_id):
    if request.method == 'OPTIONS':
        return '', 200
    veri = request.get_json()
    yeni_durum = veri.get('durum')
    database.durum_guncelle(lead_id, yeni_durum)
    return jsonify({"basari": True})
