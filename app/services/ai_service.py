import requests
from flask import current_app

class AIServiceError(Exception):
    """Yapay zeka servisi hatasi."""
    pass

class AIService:
    def _get_system_prompt(self):
        return current_app.config['BUSINESS_CONTEXT']

    def yanit_uret(self, mesaj, gecmis=None, dil="Türkçe"):
        api_key = current_app.config.get('GROQ_API_KEY')
        
        # Eger anahtar yoksa demo mesaji don (Yonerge sarti)
        if not api_key:
            return "Demo Modu: Merhaba, ben Nomi! Su an API anahtari girilmedigi icin test asamasindayim."
            
        if gecmis is None:
            gecmis = []
            
        # 1. Once sistem talimati (Dil destegi eklendi)
        system_prompt = self._get_system_prompt()
        system_prompt += f"\n\nÖNEMLİ: Ziyaretçi hangi dilde konuşursa konuşsun veya sen kim olursan ol, daima {dil} dilinde yanıt vermelisin."
        messages = [{"role": "system", "content": system_prompt}]
        
        # 2. Sonra gecmis mesajlar
        for g_msg in gecmis:
            if "role" in g_msg and "content" in g_msg:
                messages.append(g_msg)
                
        # 3. En son kullanicinin yeni mesaji
        messages.append({"role": "user", "content": mesaj})
        
        try:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "openai/gpt-oss-120b",
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 1024
            }
            
            response = requests.post(
                "https://api.groq.com/openai/v1",
                headers=headers,
                json=data,
                timeout=15
            )
            response.raise_for_status()
            
            json_response = response.json()
            return json_response['choices'][0]['message']['content']
            
        except Exception as e:
            # Hatalari yakalayip ozel hata sinifi firlat
            raise AIServiceError(f"Yapay zeka servisi iletisim hatasi: {str(e)}")

# Dosya sonunda tek bir ornek
ai_service = AIService()
