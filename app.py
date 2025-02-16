from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

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
    return jsonify({"message": "Rezerwacja zapisana!"})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
