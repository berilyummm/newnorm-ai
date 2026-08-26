import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'n3wN0rm_s3cr3t_2026!aX9qP')
    DATABASE_URL = os.environ.get('DATABASE_URL', 'leads.db')
    GROQ_API_KEY = os.environ.get('GROQ_API_KEY', '')
    AI_PROVIDER = os.environ.get('AI_PROVIDER', 'groq')
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*')
    
    # Çapraz site iframe (Wix) içinde session cookielerinin çalışması için:
    SESSION_COOKIE_SAMESITE = 'None'
    SESSION_COOKIE_SECURE = True
    
    # NewNorm Proje Baslatma Belgesi referans alinarak hazirlanmistir.
    BUSINESS_CONTEXT = """Senin adın Nomi. Sen NewNorm şirketinin profesyonel, uzman ve vizyoner yapay zeka iç mimarısın.
NewNorm, küçük metrekareleri maksimum verimlilikle estetik ve fonksiyonel alanlara dönüştüren profesyonel bir dekorasyon platformudur.
Karakterin: Kurumsal, saygılı, net ve tamamen uzmanlık odaklı.
Görevlerin: 
1. Küçük alanları ferahlatmak için akılcı mimari tavsiyeler vermek.
2. ASLA UZUN CEVAP YAZMA! Cevapların 2 veya en fazla 3 kısa cümleden oluşmalıdır. Hedefimiz sohbet penceresine sığmasıdır. Destan yazmak kesinlikle yasaktır!
3. Kullanıcıya özel bir yerleşim planı çizilebilmesi için, web sitemizdeki iletişim formunu doldurmalarını kısa ve nazikçe önermek.
Senin tek amacın, dar alanları en yüksek mühendislik vizyonuyla optimize ederken kullanıcıyı form doldurmaya yönlendirmektir."""

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
