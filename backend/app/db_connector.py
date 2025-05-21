import os
import psycopg2
from flask import jsonify
import json
from psycopg2.extras import RealDictCursor


# -------------------------
# DB-Verbindung
# -------------------------
def get_db_connection():
    return psycopg2.connect(
        host=os.environ['DB_HOST'],
        port=os.environ['DB_PORT'],
        dbname=os.environ['DB_NAME'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASS']
    )

# -------------------------
# Benutzerfunktionen
# -------------------------
def check_username(username):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM benutzer WHERE benutzername = %s", (username,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result is not None

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

def get_user(username):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, passwort, rolle FROM benutzer WHERE benutzername = %s", (username,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user

def update_user_password(user_id, hashed_password):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE benutzer SET passwort = %s WHERE id = %s
    """, (hashed_password, user_id))
    conn.commit()
    cur.close()
    conn.close()

# -------------------------
# Inventar-Funktionen
# -------------------------
def get_full_inventory():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, name, packungseinheit, ml_pro_einheit, ml_pro_vk_einheit, ek_preis, vk_preis, bild, kategorie
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
            "ml_pro_vk_einheit": row[4],
            "ek_preis": float(row[5]),
            "vk_preis": float(row[6]),
            "bild": row[7],
            "kategorie": row[8]
        } for row in rows
    ]

def get_full_inventory_by_category(kategorie):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT
            i.id, i.name, i.packungseinheit, i.ml_pro_einheit, i.ml_pro_vk_einheit,
            i.ek_preis, i.vk_preis, i.bild, i.kategorie,
            COALESCE(b.anzahl_flaschen, 0)
        FROM inventar i
        LEFT JOIN (
            SELECT DISTINCT ON (inventar_id)
                inventar_id, anzahl_flaschen
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
            "ml_pro_vk_einheit": row[4],
            "ek_preis": float(row[5]) if row[5] is not None else 0.0,
            "vk_preis": float(row[6]) if row[6] is not None else 0.0,
            "bild": row[7],
            "kategorie": row[8],
            "bestand": row[9]
        } for row in rows
    ]

def add_drink_to_inventar(data):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO inventar
        (name, packungseinheit, ml_pro_einheit, ml_pro_vk_einheit, ek_preis, vk_preis, bild, kategorie)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        data['name'],
        data['packungseinheit'],
        data['ml_pro_einheit'],
        data['ml_pro_vk_einheit'],
        data['ek_preis'],
        data['vk_preis'],
        data.get('bild'),
        data['kategorie']
    ))
    conn.commit()
    cur.close()
    conn.close()

def insert_bestand_entry(inventar_id, anzahl):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO inventar_bestand (inventar_id, anzahl_flaschen)
        VALUES (%s, %s)
    """, (inventar_id, anzahl))
    conn.commit()
    cur.close()
    conn.close()

# -------------------------
# Reporting / Auswahl
# -------------------------
def get_available_drinks():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            i.name, i.vk_preis, i.ml_pro_vk_einheit
        FROM inventar i
        JOIN (
            SELECT DISTINCT ON (inventar_id)
                inventar_id, anzahl_flaschen
            FROM inventar_bestand
            ORDER BY inventar_id, datum DESC
        ) b ON i.id = b.inventar_id
        WHERE b.anzahl_flaschen > 0;
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [
        {
            "name": row[0],
            "vk_preis": float(row[1]),
            "ml_pro_vk_einheit": row[2]
        } for row in rows
    ]

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

# -------------------------
# Test-Endpunkte
# -------------------------
def inventory_test():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM inventar LIMIT 10;")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify([
            {
                "id": row[0],
                "name": row[1],
                "packungseinheit": row[2],
                "ml_pro_einheit": row[3],
                "ml_pro_vk_einheit": row[4],
                "ek_preis": float(row[5]),
                "vk_preis": float(row[6]),
                "bild": row[7],
                "kategorie": row[8]
            } for row in rows
        ])
    except Exception as e:
        return jsonify({"error": str(e)})


##############
# Bestellung #
##############
# Bestellung speichern
def save_order(name, zutaten, preis, kundenname):
    conn = get_db_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO bestellungen (drink_name, zutaten, preis, kundenname)
                VALUES (%s, %s, %s, %s)
            """, (name, json.dumps(zutaten), preis, kundenname))

# Bestellungen abrufen (zubereitet = False → nur offene)
def get_orders(zubereitet=False):
    conn = get_db_connection()
    with conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT * FROM bestellungen
                WHERE zubereitet = %s
                ORDER BY bestellt_am DESC
            """, (bool(zubereitet),))
            return cur.fetchall()


# Bestellung als zubereitet markieren
def mark_as_prepared(bestellung_id):
    conn = get_db_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE bestellungen
                SET zubereitet = TRUE
                WHERE id = %s
            """, (bestellung_id,))
# alle 
def get_all_orders():
    conn = get_db_connection()
    with conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT * FROM bestellungen
                ORDER BY bestellt_am DESC
            """)
            return cur.fetchall()
