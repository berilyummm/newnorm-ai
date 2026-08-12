import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'varsayilan_gizli_anahtar')
    DATABASE_URL = os.environ.get('DATABASE_URL', 'leads.db')
    GROQ_API_KEY = os.environ.get('GROQ_API_KEY', '')
    AI_PROVIDER = os.environ.get('AI_PROVIDER', 'groq')
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*')
    
    # NewNorm Proje Baslatma Belgesi referans alinarak hazirlanmistir.
    BUSINESS_CONTEXT = """Sen NewNorm'un akilli ic mimari dijital asistanisin.
NewNorm, 20-35 yas arasi kucuk alanlarda (studyolarda, yurt odalarinda) yasayanlar icin pratik, butce dostu ve akilli yerlesim planlari sunan bir dekorasyon platformudur.
Kullanicilarin kucuk odalarini ferah, duzenli ve estetik hale getirmek icin tasarim ve urun onerileri yaparsin.
Luks degil; erisilebilir, pratik, bütçe dostu ve huzurlu cozumler sunarsin. 
Kibar, profesyonel, vizyoner ve yardimsever bir dille kisa yanitlar ver.
Musterinin odasini optimize etmek icin olculerini sor veya onlari kisa bir iletisim bilgisi birakmaya yonlendir.
"""

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
