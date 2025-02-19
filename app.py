from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import sqlite3
from flask_mail import Mail, Message
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Konfiguracja Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')  
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')  
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')

mail = Mail(app)

# Inicjalizacja bazy danych
def init_db():
    with sqlite3.connect("rezerwacje.db") as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS rezerwacje (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        fryzjer TEXT NOT NULL,
                        usluga TEXT NOT NULL,
                        godzina TEXT NOT NULL,
                        dzien TEXT NOT NULL,
                        email TEXT NOT NULL
                    )''')
        conn.commit()

@app.route('/')
def index():
    min_date = datetime.today().strftime('%Y-%m-%d')
    return render_template('index.html', min_date=min_date)

@app.route('/terminy', methods=['GET'])
def get_terminy():
    fryzjerzy = {
        "Krzysiek": {"uslugi": ["Strzyżenie włosów", "Broda"], "ceny": {"Strzyżenie włosów": 50, "Broda": 50, "Włosy + Broda": 85}},
        "Maciek": {"uslugi": ["Strzyżenie włosów"], "ceny": {"Strzyżenie włosów": 50}},
        "Rysiek": {"uslugi": ["Strzyżenie dzieci"], "ceny": {"Strzyżenie dzieci": 45}}
    }

    godziny = ["11:00", "12:00", "13:00", "14:00", "15:00", "16:00"]

    return jsonify({"fryzjerzy": fryzjerzy, "godziny": godziny})

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
        c.execute("SELECT * FROM rezerwacje WHERE fryzjer=? AND godzina=? AND dzien=?", (fryzjer, godzina, dzien))
        if c.fetchone():
            return jsonify({"message": "Ten termin jest już zajęty!"}), 400

        c.execute("INSERT INTO rezerwacje (fryzjer, usluga, godzina, dzien, email) VALUES (?, ?, ?, ?, ?)",
                  (fryzjer, usluga, godzina, dzien, email))
        conn.commit()

    # Wysyłanie e-maila do klienta
    try:
        msg_klient = Message("Potwierdzenie rezerwacji", recipients=[email])
        msg_klient.body = f"""Twoja rezerwacja została zapisana!

✂ Fryzjer: {fryzjer}
💇‍♂️ Usługa: {usluga}
🕒 Godzina: {godzina}
📅 Data: {dzien}

Do zobaczenia!"""
        mail.send(msg_klient)
    except Exception as e:
        print("Błąd podczas wysyłania e-maila do klienta:", str(e))

    # Wysyłanie e-maila do właściciela salonu
    try:
        msg_wlasciciel = Message("Nowa rezerwacja", recipients=["kacperskiszymon@gmail.com"])
        msg_wlasciciel.body = f"""Nowa rezerwacja w salonie fryzjerskim!

✂ Fryzjer: {fryzjer}
💇‍♂️ Usługa: {usluga}
🕒 Godzina: {godzina}
📅 Data: {dzien}
📩 Klient: {email}

Sprawdź kalendarz!"""
        mail.send(msg_wlasciciel)
    except Exception as e:
        print("Błąd podczas wysyłania e-maila do właściciela:", str(e))

    return jsonify({"message": "Rezerwacja zapisana! Powiadomienie e-mail wysłane."})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
