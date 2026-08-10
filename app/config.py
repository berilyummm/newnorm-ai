import os
from dotenv import load_dotenv

# dotenv'yi dosyanın başında çağırın
load_dotenv()

class Config:
    """Tüm ayarları ve gizli anahtarları .env dosyasından okuyan yapılandırma katmanı."""
    
    SECRET_KEY = os.environ.get('SECRET_KEY', 'guvenli-olmayan-varsayilan-anahtar')
    DATABASE_URL = os.environ.get('DATABASE_URL', 'leads.db')
    GROQ_API_KEY = os.environ.get('GROQ_API_KEY', '')
    AI_PROVIDER = os.environ.get('AI_PROVIDER', 'Groq')
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*')
    
    # Nomi (NewNorm) İşletme Asistanı Karakteri
    BUSINESS_CONTEXT = os.environ.get('BUSINESS_CONTEXT', 
        "Sen Nomi'sin. Sen 'NewNorm' adlı yenilikçi bir mimarlık firmasının Akıllı Mekan Danışmanısın. "
        "Stüdyo daireler ve küçük metrekareli evler hakkında sorulara sıcak ve profesyonel çözümler sunarsın. "
        "Kısa, öz ve enerjik yanıtlar ver. Sohbetin bir noktasında kullanıcıdan iletişim bilgisi bırakmasını iste."
    )
    
class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

# Ortama göre Config seçimi için sözlük
config_by_name = dict(
    dev=DevelopmentConfig,
    prod=ProductionConfig
)
