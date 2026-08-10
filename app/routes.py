from flask import Blueprint, request, jsonify, render_template
import datetime
from .database import lead_ekle, tum_leadler, lead_durum_guncelle, lead_sil
from .ai_service import ai_service, AIServiceError
from .whatsapp_service import send_whatsapp_notification

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
        
        # Ekstra: Mesaj saati
        saat = datetime.datetime.now().strftime("%H:%M")
        
        return jsonify({
            "basari": True, 
            "yanit": ai_yaniti,
            "saat": saat
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
    """Genişletilmiş alanlarla yeni lead kaydeder."""
    if request.method == 'OPTIONS':
        return '', 204
        
    data = request.get_json()
    isim = data.get('isim')
    soyisim = data.get('soyisim', '')
    eposta = data.get('eposta', '')
    alan_kodu = data.get('alan_kodu', '+90')
    telefon = data.get('telefon')
    butce = data.get('butce', '')
    aciklama = data.get('aciklama', '')
    mesaj = data.get('mesaj', '')
    
    # 400 hatası
    if not isim or not telefon:
        return jsonify({"basari": False, "hata": "İsim ve telefon zorunludur."}), 400
        
    try:
        # Modül B'den database.py çağrısı
        lead_ekle(isim, soyisim, eposta, alan_kodu, telefon, butce, aciklama, mesaj)
        return jsonify({"basari": True, "mesaj": "Müşteri adayı başarıyla kaydedildi."}), 201
    except Exception as e:
        return jsonify({"basari": False, "hata": f"Kayıt sırasında hata oluştu: {str(e)}"}), 500

@api_bp.route('/leads', methods=['GET'])
def get_leads():
    """Tüm lead'leri getirir."""
    try:
        leads_listesi = tum_leadler()
        return jsonify({"basari": True, "veri": leads_listesi}), 200
    except Exception as e:
        return jsonify({"basari": False, "hata": f"Veri çekilirken hata oluştu: {str(e)}"}), 500

@api_bp.route('/leads/<int:lead_id>/durum', methods=['PUT', 'OPTIONS'])
def update_lead_status(lead_id):
    """Müşteri adayının durumunu günceller ve gerekirse WhatsApp bildirimi atar."""
    if request.method == 'OPTIONS':
        return '', 204
        
    data = request.get_json()
    yeni_durum = data.get('durum') # onaylandi, reddedildi, bekliyor
    isim = data.get('isim', 'Kullanıcı')
    telefon = data.get('telefon', '')
    
    if not yeni_durum:
        return jsonify({"basari": False, "hata": "Yeni durum belirtilmedi."}), 400
        
    try:
        lead_durum_guncelle(lead_id, yeni_durum)
        
        # WhatsApp Bildirimi
        if yeni_durum in ["onaylandi", "reddedildi"] and telefon:
            send_whatsapp_notification(telefon, isim, yeni_durum)
            
        return jsonify({"basari": True, "mesaj": f"Durum '{yeni_durum}' olarak güncellendi."}), 200
    except ValueError as ve:
        return jsonify({"basari": False, "hata": str(ve)}), 404
    except Exception as e:
        return jsonify({"basari": False, "hata": str(e)}), 500

@api_bp.route('/leads/<int:lead_id>', methods=['DELETE', 'OPTIONS'])
def delete_lead(lead_id):
    """Müşteri adayını siler."""
    if request.method == 'OPTIONS':
        return '', 204
        
    try:
        lead_sil(lead_id)
        return jsonify({"basari": True, "mesaj": "Kayıt başarıyla silindi."}), 200
    except ValueError as ve:
        return jsonify({"basari": False, "hata": str(ve)}), 404
    except Exception as e:
        return jsonify({"basari": False, "hata": str(e)}), 500
