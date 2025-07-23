from flask import Flask, request, jsonify
import mysql.connector
import os

app = Flask(__name__)

db = mysql.connector.connect(
    host=os.environ.get('DB_HOST', 'localhost'),
    user=os.environ.get('DB_USER', 'root'),
    password=os.environ.get('DB_PASSWORD', 'P0o9i8u7'),
    database=os.environ.get('DB_NAME', 'notes')
)

cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS notes (id INT AUTO_INCREMENT PRIMARY KEY, text TEXT)")

@app.route('/api/notes', methods=['GET'])
def get_notes():
    cursor.execute("SELECT text FROM notes")
    notes = [{'text': row[0]} for row in cursor.fetchall()]
    return jsonify(notes)


@app.route('/api/notes', methods=['POST'])
def add_note():
    data = request.get_json()
    print("DEBUG POST DATA:", data)
    try:
        cursor.execute("INSERT INTO notes (text) VALUES (%s)", (data['text'],))
        db.commit()
        return '', 201
    except Exception as e:
        print("ERROR SAAT INSERT:", e)
        return 'Error', 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
