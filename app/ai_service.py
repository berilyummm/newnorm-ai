import requests
from .config import Config

class AIServiceError(Exception):
    """Yapay zekâ servisi ile iletişim kurulurken oluşan hatalar."""
    pass

class AIService:
    def __init__(self):
        self.api_key = Config.GROQ_API_KEY
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "llama-3.1-8b-instant"

    def _get_system_prompt(self):
        """Sistem talimatını (BUSINESS_CONTEXT) config'den okuyan yardımcı metot."""
        return Config.BUSINESS_CONTEXT

    def yanit_uret(self, mesaj, gecmis=None):
        """Kullanıcı mesajını alır, Groq servisine gönderir ve yanıtı döndürür."""
        if not self.api_key:
            return "Demo modu: API anahtarı ayarlanmamış. Ben Nomi'yim, size nasıl yardımcı olabilirim?"
            
        if gecmis is None:
            gecmis = []

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # Groq mesaj yapısı: system, gecmis mesajlar, yeni mesaj
        messages = [{"role": "system", "content": self._get_system_prompt()}]
        messages.extend(gecmis)
        messages.append({"role": "user", "content": mesaj})

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7
        }

        try:
            response = requests.post(self.api_url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            raise AIServiceError(f"Groq API hatası: {str(e)}")

# Dosya sonunda tek bir örnek oluşturulması zorunlu
ai_service = AIService()
