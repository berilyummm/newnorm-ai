from flask import Blueprint, jsonify, request, render_template
from .services.ai_service import ai_service, AIServiceError
from . import database

# Iki blueprint (Yonerge sarti)
api_bp = Blueprint('api', __name__)
pages_bp = Blueprint('pages', __name__)

# --- SAYFALAR (PAGES) ---
@pages_bp.route('/')
def index():
    return render_template('index.html')

@pages_bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# --- API UÇ NOKTALARI (API) ---

@api_bp.route('/sohbet', methods=['POST'])
def sohbet():
    veri = request.get_json()
    if not veri or 'mesaj' not in veri:
        return jsonify({'basari': False, 'hata': 'Mesaj eksik.'}), 400
        
    try:
        # AI cagrilarini try-except ile sar (Yonerge sarti)
        yanit = ai_service.yanit_uret(veri['mesaj'], veri.get('gecmis', []))
        return jsonify({'basari': True, 'yanit': yanit}), 200
    except AIServiceError as e:
        return jsonify({'basari': False, 'hata': 'Yapay zeka su an yanit veremiyor. Lutfen daha sonra tekrar deneyin.'}), 503
    except Exception:
        return jsonify({'basari': False, 'hata': 'Beklenmeyen bir hata olustu.'}), 500

@api_bp.route('/leads', methods=['POST'])
def lead_ekle_api():
    veri = request.get_json()
    if not veri or 'isim' not in veri or 'telefon' not in veri:
        return jsonify({'basari': False, 'hata': 'İsim ve telefon zorunludur.'}), 400
        
    try:
        database.lead_ekle(
            isim=veri['isim'],
            telefon=veri['telefon'],
            mesaj=veri.get('mesaj', '')
        )
        # Yeni kayitta 201 durum kodu kullanin (Yonerge sarti)
        return jsonify({'basari': True, 'mesaj': 'Kayıt basariyla olusturuldu.'}), 201
    except Exception as e:
        return jsonify({'basari': False, 'hata': 'Veritabanı hatası.'}), 500

@api_bp.route('/leads', methods=['GET'])
def lead_getir_api():
    try:
        kayitlar = database.tum_leadler()
        return jsonify({'basari': True, 'veri': kayitlar}), 200
    except Exception as e:
        return jsonify({'basari': False, 'hata': 'Kayıtlar alınamadı.'}), 500
