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
