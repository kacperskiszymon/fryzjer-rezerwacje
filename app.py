from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import sqlite3
from flask_mail import Mail, Message
import os  # 🔒 Używamy zmiennych środowiskowych do przechowywania haseł!

app = Flask(__name__)
CORS(app)

# 🔒 Konfiguracja Flask-Mail (BEZPIECZNE HASŁO)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')  # Pobiera e-mail z ENV
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')  # Pobiera hasło z ENV
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')

mail = Mail(app)

# 📌 Inicjalizacja bazy danych
def init_db():
    with sqlite3.connect("rezerwacje.db") as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS rezerwacje (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        fryzjer TEXT,
                        usluga TEXT,
                        godzina TEXT,
                        dzien TEXT,
                        email TEXT
                    )''')
        conn.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/terminy', methods=['GET'])
def get_terminy():
    terminy = {
        "Maciek": {"uslugi": ["Strzyżenie męskie", "Broda"], "cena": "50 zł"},
        "Krzysiek": {"uslugi": ["Strzyżenie + Broda"], "cena": "80 zł"},
        "Rysiek": {"uslugi": ["Strzyżenie dzieci"], "cena": "40 zł"}
    }
    godziny = ["11:00", "12:00", "13:00", "14:00", "15:00", "16:00"]
    
    return jsonify({"fryzjerzy": terminy, "godziny": godziny})

@app.route('/rezerwuj', methods=['POST'])
def rezerwuj():
    data = request.json
    fryzjer = data.get('fryzjer')
    usluga = data.get('usluga')
    godzina = data.get('godzina')
    dzien = data.get('dzien')
    email = data.get('email')

    if not fryzjer or not usluga or not godzina or not dzien or not email:
        return jsonify({"message": "Wypełnij wszystkie pola!"}), 400

    with sqlite3.connect("rezerwacje.db") as conn:
        c = conn.cursor()
        
        # ✅ Sprawdź, czy termin nie jest już zajęty!
        c.execute("SELECT * FROM rezerwacje WHERE fryzjer=? AND godzina=? AND dzien=?", (fryzjer, godzina, dzien))
        if c.fetchone():
            return jsonify({"message": "Ten termin jest już zajęty!"}), 400

        # ✅ Zapisz rezerwację
        c.execute("INSERT INTO rezerwacje (fryzjer, usluga, godzina, dzien, email) VALUES (?, ?, ?, ?, ?)",
                  (fryzjer, usluga, godzina, dzien, email))
        conn.commit()

    # 📩 Wysyłanie e-maila z potwierdzeniem
    try:
        msg = Message("Potwierdzenie rezerwacji", recipients=[email])
        msg.body = f"""Twoja rezerwacja została zapisana!
        
        ✂ Fryzjer: {fryzjer}
        💇‍♂️ Usługa: {usluga}
        🕒 Godzina: {godzina}
        📅 Data: {dzien}

        Do zobaczenia!
        """
        mail.send(msg)
    except Exception as e:
        print("Błąd podczas wysyłania e-maila:", str(e))

    return jsonify({"message": "Rezerwacja zapisana! Powiadomienie e-mail wysłane."})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
