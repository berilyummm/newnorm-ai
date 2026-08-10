from flask import Blueprint, request, jsonify, render_template
from .database import lead_ekle, tum_leadler
from .ai_service import ai_service, AIServiceError

# İki Blueprint: Biri API işlemleri, diğeri sayfalar (HTML) için
api_bp = Blueprint('api', __name__)
page_bp = Blueprint('pages', __name__)

# --- SAYFALAR (HTML) ---
@page_bp.route('/', methods=['GET'])
def index():
    """Karşılama sayfasını gösterir."""
    return render_template('index.html')

@page_bp.route('/dashboard', methods=['GET'])
def dashboard():
    """Yönetim panelini gösterir."""
    return render_template('dashboard.html')


# --- API UÇ NOKTALARI ---
@api_bp.route('/sohbet', methods=['POST', 'OPTIONS'])
def sohbet():
    """AI'a mesaj iletir."""
    if request.method == 'OPTIONS':
        return '', 204
        
    data = request.get_json()
    if not data or 'mesaj' not in data:
        return jsonify({"basari": False, "hata": "Eksik veri: 'mesaj' alanı gerekli."}), 400
        
    kullanici_mesaji = data.get('mesaj')
    gecmis_mesajlar = data.get('gecmis', [])
    
    try:
        # Modül C'den ai_service objesi üzerinden fonksiyon çağrısı
        ai_yaniti = ai_service.yanit_uret(kullanici_mesaji, gecmis_mesajlar)
        return jsonify({
            "basari": True, 
            "yanit": ai_yaniti
        }), 200
    except AIServiceError as e:
        # AI hatası olursa 503 durum kodu
        return jsonify({
            "basari": False, 
            "hata": "Yapay zekâ servisinde geçici bir sorun var.",
            "detay": str(e)
        }), 503

@api_bp.route('/leads', methods=['POST', 'OPTIONS'])
def create_lead():
    """Yeni lead kaydeder."""
    if request.method == 'OPTIONS':
        return '', 204
        
    data = request.get_json()
    isim = data.get('isim')
    telefon = data.get('telefon')
    mesaj = data.get('mesaj', '')
    
    # 400 hatası
    if not isim or not telefon:
        return jsonify({"basari": False, "hata": "İsim ve telefon zorunludur."}), 400
        
    try:
        # Modül B'den database.py çağrısı
        lead_ekle(isim, telefon, mesaj)
        # Yeni kayıtta 201 durum kodu
        return jsonify({"basari": True, "mesaj": "Müşteri adayı başarıyla kaydedildi."}), 201
    except Exception as e:
        return jsonify({"basari": False, "hata": f"Kayıt sırasında hata oluştu: {str(e)}"}), 500

@api_bp.route('/leads', methods=['GET'])
def get_leads():
    """Tüm lead'leri getirir."""
    try:
        # Modül B'den database.py çağrısı
        leads_listesi = tum_leadler()
        return jsonify({"basari": True, "veri": leads_listesi}), 200
    except Exception as e:
        return jsonify({"basari": False, "hata": f"Veri çekilirken hata oluştu: {str(e)}"}), 500
