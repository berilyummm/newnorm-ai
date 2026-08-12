from flask import Flask, jsonify
from flask_cors import CORS
from config import config

def create_app(config_name='default'):
    app = Flask(__name__)
    
    # 1. Ayarlari yukle
    app.config.from_object(config[config_name])
    
    # 2. CORS ac (Wix'ten gelen isteklere izin ver)
    CORS(app, resources={r"/api/*": {"origins": app.config['CORS_ORIGINS']}})
    
    # 3. Veritabanini baslat (init_db)
    from . import database
    database.init_db(app)
    
    # 4. Blueprint'leri kaydet
    from .routes import api_bp, pages_bp
    app.register_blueprint(pages_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # 5. /health uc noktasi (Sunucu canlilik kontrolu)
    @app.route('/health')
    def health_check():
        return jsonify({"status": "aktif", "message": "Sunucu calisiyor."}), 200
        
    return app
