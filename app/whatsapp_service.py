import datetime

def send_whatsapp_notification(telefon, isim, durum):
    """
    WhatsApp bildirim simülasyonu.
    Gerçek bir projede buraya Twilio veya Meta WhatsApp Business API entegrasyonu yazılır.
    Şu an için konsola ve log'lara yazdırıyoruz.
    """
    saat = datetime.datetime.now().strftime("%H:%M:%S")
    
    mesaj = ""
    if durum == "onaylandi":
        mesaj = f"Merhaba {isim}, NewNorm ile olan görüşme talebiniz onaylanmıştır! En kısa sürede sizinle iletişime geçeceğiz."
    elif durum == "reddedildi":
        mesaj = f"Merhaba {isim}, talebinizi şu an için değerlendiremiyoruz. İlginiz için teşekkürler."
    else:
        return False

    # GERÇEK BİR SİSTEMDE BURASI REQUESTS.POST İLE API'YE GİDECEKTİR
    print("\n" + "="*50)
    print(f"🟢 [WHATSAPP SIMULASYONU] Saat: {saat}")
    print(f"Gönderilen Numara: {telefon}")
    print(f"Mesaj: {mesaj}")
    print("="*50 + "\n")
    
    return True
