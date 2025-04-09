import os
import psycopg2
from flask import Flask, jsonify

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

def get_db_connection():
    return psycopg2.connect(
        host=os.environ['DB_HOST'],
        port=os.environ['DB_PORT'],
        dbname=os.environ['DB_NAME'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASS']
    )