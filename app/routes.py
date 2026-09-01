# ========================================================
# NOMI AI - GROQ (LLAMA 3) BAĞLANTISI (HIZLANDIRILMIŞ)
# ========================================================

@api_bp.route('/sohbet', methods=['POST', 'OPTIONS'])
def sohbet_api():
    if request.method == 'OPTIONS':
        return '', 200
        
    veri = request.get_json()
    kullanici_mesaji = veri.get('mesaj', '')
    
    api_key = os.environ.get("GROQ_API_KEY") or os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return jsonify({"basari": True, "yanit": "Sistem hatası: GROQ API anahtarı Render'da bulunamadı!"})
        
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # 1. Nomi'nin Kişiliği: Kesinlikle çok kısa konuşması emredildi
    sistem_talimati = """
    Senin adın Nomi. Sen 'NewNorm' şirketinin resmi yapay zeka asistanısın.
    Amacın: Büyük şehirlerde küçük evlerde yaşayan insanlara akıllı yaşam tarzı ve ferahlatıcı dekorasyon tavsiyeleri vermektir.
    Kullanıcılara zekice ve bütçe dostu çözümler sunarsın.
    KESİN KURAL: Cevaplarını her zaman KESİNLİKLE çok kısa, net ve en fazla 1-2 cümle olarak vermelisin. Asla uzun listeler veya paragraflar yazma. Samimi ve nokta atışı konuş.
    """
    
    # 2. Jet Hızındaki Model ve Token (Kelime) Sınırı eklendi
    data = {
        "model": "llama3-8b-8192", # Groq'un en hafif ve en hızlı modeli
        "messages": [
            {"role": "system", "content": sistem_talimati},
            {"role": "user", "content": kullanici_mesaji}
        ],
        "temperature": 0.7,
        "max_tokens": 100 # Bu satır yapay zekanın fazla düşünmesini kesip anında cevap vermesini sağlar
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response_json = response.json()
        
        if "error" in response_json:
            return jsonify({"basari": True, "yanit": f"Groq Hatası: {response_json['error']['message']}"})
            
        yanit = response_json['choices'][0]['message']['content']
        
        return jsonify({"basari": True, "yanit": yanit})
        
    except Exception as e:
        hata_mesaji = f"Sistem Hatası Detayı: {str(e)}"
        return jsonify({"basari": True, "yanit": hata_mesaji})
