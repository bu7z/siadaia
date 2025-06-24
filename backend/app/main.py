# libaries
import os
from dotenv import load_dotenv
import psycopg2
from flask import Flask, jsonify, request, Response
from flask_cors import CORS
import bcrypt
from flask_jwt_extended import JWTManager, create_access_token
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask_jwt_extended.exceptions import NoAuthorizationError
import traceback
import time

# files
import db_connector
import openai_connector
from object_detector import generate_camera_stream, person_count, person_count_lock, cleanup, get_person_count

load_dotenv()

app = Flask(__name__)
CORS(app, origins="*", supports_credentials=True)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config["JWT_TOKEN_LOCATION"] = ["headers"]
app.config["JWT_HEADER_NAME"] = "Authorization"
app.config["JWT_HEADER_TYPE"] = "Bearer"

jwt = JWTManager(app) 

###########
# Testing #
###########

@app.route('/')
def hello():
    return "Hello from Flask!"

@app.route('/api/test-db')
def test_db():
    return db_connector.db_test()

@app.route('/api/status')
def status():
    return jsonify({"status": "OK"})

# Inventar #
@app.route('/api/test-inventory')
def test_inventory():
    return db_connector.inventory_test()

# Bestand #
@app.route('/api/test-bestand')
def test_bestand():
    return db_connector.bestand_test()

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

    if not username or not password:
        return jsonify({'success': False, 'message': 'Benutzername und Passwort sind erforderlich'}), 400

    if db_connector.check_username(username):
        return jsonify({'success': False, 'message': 'Benutzername bereits vergeben'}), 409

    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    db_connector.create_user(username, hashed_pw, vorname, nachname)

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

    user = db_connector.get_user(username)
    if user and bcrypt.checkpw(password.encode('utf-8'), user[1].encode('utf-8')):
        token = create_access_token(identity=username, additional_claims={
            'id': user[0],
            'rolle': user[2]
        })
        return jsonify({'success': True, 'message': 'Login erfolgreich', 'token': token})

    return jsonify({'success': False, 'message': 'Login fehlgeschlagen'}), 401

##########
# Logout #
##########
@app.route('/api/change-password', methods=['POST'])
@jwt_required()
def change_password():
    data = request.get_json()
    new_password = data.get('new_password')
    user_id = get_jwt().get("id")

    if not new_password:
        return jsonify({"success": False, "message": "Neues Passwort fehlt"}), 400

    try:
        hashed_pw = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        db_connector.update_user_password(user_id, hashed_pw)
        return jsonify({"success": True, "message": "Passwort erfolgreich geändert"})
    except Exception as e:
        print("Fehler beim Passwort-Update:", e)
        return jsonify({"success": False, "message": "Fehler beim Aktualisieren"}), 500

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

#################
# Chart Bestand #
#################
@app.route('/api/bestand', methods=['GET'])
@jwt_required()
def get_inventory_bestand():
    try:
        rows = db_connector.get_bestand()
        result = [
            {
                "id": row[0],
                "inventar_id": row[1],
                "produktname": row[2],
                "datum": row[3].isoformat(),
                "anzahl": row[4]
            }
            for row in rows
        ]
        return jsonify({"inventar": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

##################
# Drink Advisory #
##################
@app.route('/api/beratung', methods=['POST'])
def beratung():
    data = request.get_json()
    drinks_available = db_connector.get_available_drinks()
    response_msg = openai_connector.get_drink_recommendation(
        data.get('vibe'),
        data.get('preferences', []),
        drinks_available
    )
    return jsonify({"success": True, "drink": response_msg})

@app.route('/api/check', methods=['POST'])
def check():
    data = request.get_json()
    drink = data.get('drink', '')
    if "aschenbecher" in drink.lower():
        return jsonify({"success": True, "drink": "Club Mate ...\nLuL"})

    drinks_available = db_connector.get_available_drinks()
    inquiry_check = openai_connector.validate_drink_inquiry(drink, drinks_available)
    return jsonify({"success": True, "drink": inquiry_check})

@app.route('/api/examples', methods=['GET'])
def create():
    try:
        drinks_available = db_connector.get_available_drinks()
        examples_drinks = openai_connector.create_example_drinks(drinks_available)
        return jsonify({"success": True, "drinks": examples_drinks})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500

####################
# Object Detection #
####################
@app.route('/api/camera-feed-<cam>')
def camera_feed(cam):
    try:
        cam_type = 1 if cam == 'sto' else 2
        return Response(
            generate_camera_stream(cam_type),
            mimetype='multipart/x-mixed-replace; boundary=frame',
            headers={
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'X-Accel-Buffering': 'no'
            }
        )
    except Exception as e:
        print(f"Fehler in camera-feed-{cam}: {str(e)}")
        return jsonify({"error": "Camera feed unavailable"}), 500

@app.route('/api/person-count', methods=['GET'])
def handle_person_count():
    try:
        return jsonify({
            "count": get_person_count(),
            "timestamp": time.time()
        })
    except Exception as e:
        return jsonify({
            "count": 0,
            "error": str(e),
            "timestamp": time.time()
        }), 500

@app.teardown_appcontext
def shutdown(exception=None):
    cleanup()


#########
# Stock #
#########
@app.route('/api/inventar', methods=['GET'])
@jwt_required()
def get_inventar():
    try:
        items = db_connector.get_full_inventory()
        return jsonify({"success": True, "inventar": items})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/bestand-kategorie/<kategorie>', methods=['GET'])
@jwt_required()
def bestand_nach_kategorie(kategorie):
    try:
        daten = db_connector.get_full_inventory_by_category(kategorie)
        return jsonify({"data": daten})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/api/inventar', methods=['POST'])
@jwt_required()
def add_drink():
    try:
        data = request.get_json()
        required_fields = ['name', 'packungseinheit', 'ml_pro_einheit', 'ek_preis', 'vk_preis', 'kategorie']
        if not all(field in data for field in required_fields):
            return jsonify({"success": False, "message": "Unvollständige Angaben"}), 400

        db_connector.add_drink_to_inventar(data)
        return jsonify({"success": True, "message": "Getränk erfolgreich hinzugefügt"})
    except Exception as e:
        return jsonify({"success": False, "message": f"Serverfehler: {str(e)}"}), 500

@app.route('/api/bestand', methods=['POST'])
@jwt_required()
def add_bestand_entry():
    try:
        data = request.get_json()
        if not data.get("inventar_id") or not data.get("anzahl"):
            return jsonify({"success": False, "message": "Fehlende Daten"}), 400

        db_connector.insert_bestand_entry(data["inventar_id"], data["anzahl"])
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

######################
# Bestellungen/Order #
######################
@app.route('/api/bestellungen', methods=['POST'])
def bestellung_absenden():
    try:
        data = request.get_json()
        required = ['drink_name', 'zutaten', 'preis', 'kundenname']
        for field in required:
            if field not in data:
                return jsonify({"success": False, "message": f"Feld fehlt: {field}"}), 400

        if not isinstance(data['zutaten'], list):
            return jsonify({"success": False, "message": "Zutaten müssen ein Array sein"}), 400

        db_connector.save_order(
            data['drink_name'],
            data['zutaten'],
            data['preis'],
            data['kundenname']
        )
        return jsonify({"success": True})
    except Exception as e:
        print("❌ Fehler bei Bestellung:", e)
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/bestellungen', methods=['GET'])
@jwt_required()
def get_bestellungen():
    try:
        return jsonify(db_connector.get_orders(zubereitet=False))
    except Exception as e:
        print("Fehler beim Laden der Bestellungen:", e)
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/bestellungen/alle', methods=['GET'])
@jwt_required()
def get_alle_bestellungen():
    try:
        return jsonify(db_connector.get_all_orders())
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/bestellungen/<int:bestellung_id>/zubereitet', methods=['PATCH'])
@jwt_required()
def markiere_zubereitet(bestellung_id):
    try:
        db_connector.mark_as_prepared(bestellung_id)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
    
@app.route('/api/bestellungen/vergangene', methods=['GET'])
@jwt_required()
def get_vergangene_bestellungen():
    try:
        return jsonify(db_connector.get_orders(zubereitet=True))
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.teardown_appcontext
def shutdown(exception=None):
    cleanup()


##############################
# Endpoint for visitor Stats #
##############################
@app.route('/api/person-history', methods=['GET'])
@jwt_required()
def get_person_history():
    try:
        result = db_connector.get_person_counts()
        return jsonify({"person_count": result})
    except Exception as e:
        print("Fehler bei /api/person-history:", e)
        return jsonify({"success": False, "message": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
