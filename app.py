from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import sqlite3
from flask_mail import Mail, Message  # 📩 Importujemy Flask-Mail

app = Flask(__name__)
CORS(app)

# Konfiguracja Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'kacperskiszymon@gmail.com'  # Twój e-mail
app.config['MAIL_PASSWORD'] = 'uhxs ziuz nitm yuux'  # Hasło aplikacji
app.config['MAIL_DEFAULT_SENDER'] = 'kacperskiszymon@gmail.com'  # Nadawca e-maila

mail = Mail(app)

# Inicjalizacja bazy danych
def init_db():
    with sqlite3.connect("rezerwacje.db") as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS rezerwacje (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        fryzjer TEXT,
                        usluga TEXT,
                        godzina TEXT,
                        dzien TEXT
                    )''')
        conn.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/terminy', methods=['GET'])
def get_terminy():
    terminy = {
        "Maciek": ["Strzyżenie męskie", "Broda"],
        "Krzysiek": ["Strzyżenie + Broda"],
        "Rysiek": ["Strzyżenie dzieci"]
    }
    godziny = ["11:00", "12:00", "13:00", "14:00", "15:00", "16:00"]
    return jsonify({"fryzjerzy": terminy, "godziny": godziny})

@app.route('/rezerwuj', methods=['POST'])
def rezerwuj():
    data = request.json
    fryzjer = data['fryzjer']
    usluga = data['usluga']
    godzina = data['godzina']
    dzien = data['dzien']

    with sqlite3.connect("rezerwacje.db") as conn:
        c = conn.cursor()
        c.execute("INSERT INTO rezerwacje (fryzjer, usluga, godzina, dzien) VALUES (?, ?, ?, ?)",
                  (fryzjer, usluga, godzina, dzien))
        conn.commit()

    # Wysyłanie e-maila z potwierdzeniem rezerwacji
    try:
        msg = Message("Potwierdzenie rezerwacji",
                      recipients=["klient@example.com"])  # Podmień na rzeczywisty e-mail klienta
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
