import os
import psycopg2
from flask import Flask, jsonify
import bcrypt
from flask_jwt_extended import JWTManager, create_access_token

# Testing
def db_test():
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
    

def inventory_test():
    try:
        conn = psycopg2.connect(
            host=os.environ['DB_HOST'],
            port=os.environ['DB_PORT'],
            dbname=os.environ['DB_NAME'],
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASS']
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM inventar LIMIT 10;")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        # Optional: Umwandeln in JSON-freundliches Format
        
        spirits = [
            {
                "id": row[0],
                "Name": row[1],
                "Packungseinheit": row[2],
                "ML pro Einheit": row[3],
                "EK": row[4],
                "VK": row[5],
                "Produktbild": row[6]
            } for row in rows
        ]
        
        return jsonify({"inventar": spirits})
    except Exception as e:
        return jsonify({"error": str(e)})
    

def bestand_test():
    try:
        conn = psycopg2.connect(
            host=os.environ['DB_HOST'],
            port=os.environ['DB_PORT'],
            dbname=os.environ['DB_NAME'],
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASS']
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM inventar_bestand LIMIT 10;")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        # Optional: Umwandeln in JSON-freundliches Format
        
        spirits = [
            {
                "id": row[0],
                "inventar_id": row[1],
                "Datum": row[2],
                "Anzahl": row[3],
            } for row in rows
        ]
        
        return jsonify({"inventar": spirits})
    except Exception as e:
        return jsonify({"error": str(e)})

    


#################
# Registrierung #
#################
def check_username(username):
    conn = get_db_connection()
    cur = conn.cursor()

    # Prüfen, ob Benutzername schon existiert
    cur.execute("SELECT id FROM benutzer WHERE benutzername = %s", (username,))
    if cur.fetchone():
        cur.close()
        conn.close()
        return True

def create_user(username, hashed_pw, vorname, nachname):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO benutzer (benutzername, passwort, vorname, nachname, rolle)
        VALUES (%s, %s, %s, %s, %s)
    """, (username, hashed_pw, vorname, nachname, 'user'))

    conn.commit()
    cur.close()
    conn.close()

#########
# Login #
#########
def get_user(username):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, passwort, rolle FROM benutzer WHERE benutzername = %s", (username,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user

##########
# Logout #
##########
def update_user_password(user_id, hashed_password):
    conn = get_db_connection()
    cur = conn.cursor()
    query = """
        UPDATE benutzer
        SET passwort = %s
        WHERE id = %s
    """
    cur.execute(query, (hashed_password, user_id))
    conn.commit()
    cur.close()
    conn.close()

#################
# Chart Bestand #
#################
def get_bestand():

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT ib.id, ib.inventar_id, i.name, ib.datum, ib.anzahl_flaschen
        FROM inventar_bestand ib
        JOIN inventar i ON ib.inventar_id = i.id
        ORDER BY ib.datum ASC
    """)

    rows = cur.fetchall()
    cur.close()
    conn.close()

    return rows

#####################
# Beratung - Drinks #
#####################
def get_available_drinks():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT 
            i.name,
            i.vk_preis,
            i.ml_pro_einheit
        FROM inventar i
        JOIN (
            SELECT DISTINCT ON (inventar_id)
                inventar_id,
                anzahl_flaschen
            FROM inventar_bestand
            ORDER BY inventar_id, datum DESC
        ) b ON i.id = b.inventar_id
        WHERE b.anzahl_flaschen > 0;
    """)

    rows = cur.fetchall()
    result = [
        {
            "name": row[0],
            "vk_preis": float(row[1]),
            "ml_pro_einheit": row[2]
        }
        for row in rows
    ]

    cur.close()
    conn.close()
    return result


#########
# Stock #
#########
def get_full_inventory():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, name, packungseinheit, ml_pro_einheit, ek_preis, vk_preis, bild, kategorie
        FROM inventar
        ORDER BY kategorie, name;
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [
        {
            "id": row[0],
            "name": row[1],
            "packungseinheit": row[2],
            "ml_pro_einheit": row[3],
            "ek_preis": float(row[4]),
            "vk_preis": float(row[5]),
            "bild": row[6],
            "kategorie": row[7]
        }
        for row in rows
    ]
# table + chart
def get_full_inventory_by_category(kategorie):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT
            i.id,
            i.name,
            i.packungseinheit,
            i.ml_pro_einheit,
            i.ek_preis,
            i.vk_preis,
            i.bild,
            i.kategorie,
            COALESCE(b.anzahl_flaschen, 0) as bestand
        FROM inventar i
        LEFT JOIN (
            SELECT DISTINCT ON (inventar_id)
                inventar_id,
                anzahl_flaschen
            FROM inventar_bestand
            ORDER BY inventar_id, datum DESC
        ) b ON i.id = b.inventar_id
        WHERE i.kategorie = %s
        ORDER BY i.name
    """, (kategorie,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [
        {
            "id": row[0],
            "name": row[1],
            "packungseinheit": row[2],
            "ml_pro_einheit": row[3],
            "ek_preis": float(row[4]),
            "vk_preis": float(row[5]),
            "bild": row[6],
            "kategorie": row[7],
            "bestand": row[8]
        }
        for row in rows
    ]
# add unit
def add_drink_to_inventar(data):
    conn = get_db_connection()
    cur = conn.cursor()

    query = """
        INSERT INTO inventar
        (name, packungseinheit, ml_pro_einheit, ek_preis, vk_preis, kategorie)
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    values = (
        data['name'],
        data['packungseinheit'],
        data['ml_pro_einheit'],
        data['ek_preis'],
        data['vk_preis'],
        data['kategorie']
    )

    cur.execute(query, values)
    conn.commit()
    cur.close()
    conn.close()




def get_db_connection():
    return psycopg2.connect(
        host=os.environ['DB_HOST'],
        port=os.environ['DB_PORT'],
        dbname=os.environ['DB_NAME'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASS']
    )