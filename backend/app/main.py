import os
import psycopg2
from flask import Flask, jsonify


app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello from Flask!"



@app.route('/api/test-db')
def test_db():
    try:
        conn = psycopg2.connect(
            host=os.environ['DB_HOST'],
            port=os.environ['DB_PORT'],
            dbname=os.environ['DB_NAME'],
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASS']
        )
        cursor = conn.cursor()
        cursor.execute("SELECT id, benutzername, vorname, nachname, rolle FROM benutzer LIMIT 10;")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        # Optional: Umwandeln in JSON-freundliches Format
        users = [
            {
                "id": row[0],
                "benutzername": row[1],
                "vorname": row[2],
                "nachname": row[3],
                "rolle": row[4]
            } for row in rows
        ]

        return jsonify({"benutzer": users})
    except Exception as e:
        return jsonify({"error": str(e)})




@app.route('/api/status')
def status():
    return jsonify({"status": "OK"})










if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
