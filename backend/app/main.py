# libaries
import os
from dotenv import load_dotenv
import psycopg2
from flask import Flask, jsonify, request
from flask_cors import CORS
import bcrypt
from flask_jwt_extended import JWTManager, create_access_token
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask_jwt_extended.exceptions import NoAuthorizationError

# files
import db_connector


load_dotenv()

app = Flask(__name__)
CORS(app, origins="*", supports_credentials=True) # Einschränkung CORS auf Frontend, bei Servertrennung localhost anpassen
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config["JWT_TOKEN_LOCATION"] = ["headers"]
app.config["JWT_HEADER_NAME"] = "Authorization"
app.config["JWT_HEADER_TYPE"] = "Bearer"

jwt = JWTManager(app) 


# Testing

@app.route('/')
def hello():
    return "Hello from Flask!"

@app.route('/api/test-db')
def test_db():
    return db_connector.function_db_test()

@app.route('/api/status')
def status():
    return jsonify({"status": "OK"})


#################
# Registrierung #
#################
@app.route('/api/register', methods=['POST'])
def register_user():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')
    vorname = data.get('vorname')
    nachname = data.get('nachname')
    print("test")

    if not username or not password:
        return jsonify({'success': False, 'message': 'Benutzername und Passwort sind erforderlich'}), 400

    conn = db_connector.get_db_connection()
    cur = conn.cursor()

    # Prüfen, ob Benutzername schon existiert
    cur.execute("SELECT id FROM benutzer WHERE benutzername = %s", (username,))
    if cur.fetchone():
        cur.close()
        conn.close()
        return jsonify({'success': False, 'message': 'Benutzername bereits vergeben'}), 409

    # Passwort hashen
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Neuen Benutzer einfügen
    cur.execute("""
        INSERT INTO benutzer (benutzername, passwort, vorname, nachname, rolle)
        VALUES (%s, %s, %s, %s, %s)
    """, (username, hashed_pw, vorname, nachname, 'user'))

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({'success': True, 'message': 'Registrierung erfolgreich'})


#########
# Login #
#########
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'success': False, 'message': 'Benutzername und Passwort erforderlich'}), 400

    conn = db_connector.get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, passwort, rolle FROM benutzer WHERE benutzername = %s", (username,))
    user = cur.fetchone()

    if user and bcrypt.checkpw(password.encode('utf-8'), user[1].encode('utf-8')):
        user_id = user[0]
        rolle = user[2]
        token = create_access_token(identity=username, additional_claims={
        'id': user_id,
        'rolle': rolle
    })
        return jsonify({'success': True, 'message': 'Login erfolgreich', 'token': token})

    return jsonify({'success': False, 'message': 'Login fehlgeschlagen'}), 401


#######################
# Token-Verifizierung #
#######################
@app.route('/api/verify-token', methods=['GET'])
@jwt_required()
def verify_token():
    return jsonify(success=True, user={
        "username": get_jwt_identity(),
        "id": get_jwt().get("id"),
        "rolle": get_jwt().get("rolle")
    })






if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
