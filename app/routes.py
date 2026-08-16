from flask import Blueprint, jsonify, request, render_template, session, redirect, url_for
from .services.ai_service import ai_service, AIServiceError
from . import database

# --- KONTROL KATMANI (CONTROLLER) - SEPARATION OF CONCERNS (SoC) ---
# Bu dosya SADECE gelen HTTP isteklerini yönlendirmekten sorumludur.
# Veritabanı işlemleri database.py'ye, yapay zeka mantığı ise ai_service.py'ye bırakılmıştır.

# Yönerge Şartı: İki blueprint ile API ve sayfa rotaları temiz bir şekilde ayrılmıştır.
api_bp = Blueprint('api', __name__)
pages_bp = Blueprint('pages', __name__)

# --- SAYFALAR (PAGES) ---
@pages_bp.route('/')
def index():
    return render_template('index.html')

@pages_bp.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('pages.login'))
    return render_template('dashboard.html')

@pages_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        kullanici = request.form.get('username')
        sifre = request.form.get('password')
        if kullanici == 'admin' and sifre == 'newnorm':
            session['logged_in'] = True
            return redirect(url_for('pages.dashboard'))
        else:
            return render_template('login.html', hata="Hatalı kullanıcı adı veya şifre!")
    return render_template('login.html')

@pages_bp.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('pages.login'))

# --- API UÇ NOKTALARI (API) ---

@api_bp.route('/sohbet', methods=['POST'])
def sohbet():
    veri = request.get_json()
    if not veri or 'mesaj' not in veri:
        return jsonify({'basari': False, 'hata': 'Mesaj eksik.'}), 400
        
    try:
        # Wix'ten gelen 'dil' parametresini al, gelmezse Türkçe (veya sitenin ana dili) kabul et
        dil = veri.get('dil', 'Türkçe')
        
        # AI cagrilarini try-except ile sar (Yonerge sarti)
        yanit = ai_service.yanit_uret(veri['mesaj'], veri.get('gecmis', []), dil=dil)
        return jsonify({'basari': True, 'yanit': yanit}), 200
    except AIServiceError as e:
        # Yönerge Şartı: try-except ile "Kibar hata yanıtları" dönülür. 503 Service Unavailable
        return jsonify({'basari': False, 'hata': 'Yapay zeka şu an yoğun, lütfen birazdan tekrar deneyin.'}), 503
    except Exception:
        # 500 Internal Server Error
        return jsonify({'basari': False, 'hata': 'Beklenmeyen bir sunucu hatası oluştu.'}), 500

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
        # Hata Yönetimi: Kullanıcıya kibar hata mesajı
        return jsonify({'basari': False, 'hata': 'Üzgünüz, veritabanı bağlantısında bir sorun oluştu.'}), 500

def check_auth_or_apikey():
    if session.get('logged_in'):
        return True
    if request.headers.get('X-Admin-Key') == 'newnorm2026':
        return True
    return False

@api_bp.route('/leads', methods=['GET'])
def lead_getir_api():
    if not check_auth_or_apikey():
        return jsonify({'basari': False, 'hata': 'Yetkisiz erişim.'}), 401
    try:
        kayitlar = database.tum_leadler()
        return jsonify({'basari': True, 'veri': kayitlar}), 200
    except Exception as e:
        return jsonify({'basari': False, 'hata': 'Kayıtlar alınamadı.'}), 500

@api_bp.route('/leads/<int:lead_id>/durum', methods=['PUT'])
def lead_durum_guncelle_api(lead_id):
    if not check_auth_or_apikey():
        return jsonify({'basari': False, 'hata': 'Yetkisiz erişim.'}), 401
    veri = request.get_json()
    if not veri or 'durum' not in veri:
        return jsonify({'basari': False, 'hata': 'Durum bilgisi eksik.'}), 400
        
    try:
        database.durum_guncelle(lead_id, veri['durum'])
        return jsonify({'basari': True, 'mesaj': 'Durum güncellendi.'}), 200
    except Exception as e:
        return jsonify({'basari': False, 'hata': 'Veritabanı hatası.'}), 500

@api_bp.route('/leads/<int:lead_id>', methods=['DELETE'])
def lead_sil_api(lead_id):
    if not check_auth_or_apikey():
        return jsonify({'basari': False, 'hata': 'Yetkisiz erişim.'}), 401
    try:
        database.lead_sil(lead_id)
        return jsonify({'basari': True, 'mesaj': 'Kayıt silindi.'}), 200
    except Exception as e:
        return jsonify({'basari': False, 'hata': 'Veritabanı hatası.'}), 500
