from app import create_app

# Flask uygulamasını oluştur
app = create_app()

if __name__ == '__main__':
    # Sadece yerel geliştirmede çalışacak kod bloğu
    # Render (Gunicorn) burayı çalıştırmaz, doğrudan 'app' objesini hedefler.
    app.run(debug=True, host='0.0.0.0', port=5000)
