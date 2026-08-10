from flask import Flask, jsonify
from flask_cors import CORS
from .config import Config
from .database import init_db

def create_app():
    """
    Ayarları, CORS'u, veritabanını ve rotaları bir araya getiren fabrika fonksiyonu.
    """
    app = Flask(__name__)
    
    # 1. Ayarları Yükle
    app.config.from_object(Config)
    
    # 2. CORS Aç
    CORS(app, resources={r"/api/*": {"origins": app.config['CORS_ORIGINS']}})
    
    # 3. Veritabanını Başlat (app_context içinde)
    with app.app_context():
        init_db(app)
        
    # 4. Blueprint'leri Kaydet
    from .routes import api_bp, page_bp
    app.register_blueprint(page_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # 5. Sunucu Canlılık Kontrolü (Health Endpoint)
    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({"durum": "aktif", "mesaj": "Sistem sorunsuz çalışıyor."}), 200
        
    return app
