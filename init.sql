CREATE TABLE IF NOT EXISTS benutzer (
    id SERIAL PRIMARY KEY,
    benutzername VARCHAR(50) UNIQUE NOT NULL,
    passwort TEXT NOT NULL,
    vorname VARCHAR(100),
    nachname VARCHAR(100),
    rolle VARCHAR(50),
    erstellt_am TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS inventar (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    packungseinheit INTEGER NOT NULL,         -- z. B. Anzahl der Flaschen pro Kasten/Paket
    ml_pro_einheit INTEGER NOT NULL,          -- z. B. 700 ml pro Flasche
    ml_pro_vk_einheit INTEGER NOT NULL,
    ek_preis NUMERIC(10, 2) NOT NULL,         -- Einkaufspreis pro Flasche
    vk_preis NUMERIC(10, 2) NOT NULL,         -- Verkaufspreis
    bild TEXT,                                -- z. B. Pfad oder URL zum Bild (kann NULL sein)
    kategorie VARCHAR(50),                    -- z. B. Biere, Spirituosen, Softdrinks 0,33l
    erstellt_am TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS inventar_bestand (
    id SERIAL PRIMARY KEY,
    inventar_id INTEGER REFERENCES inventar(id),
    datum TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    anzahl_flaschen INTEGER NOT NULL
);

-- table for person count (only Di & Do Night?)
CREATE TABLE person_count (
    timestamp TIMESTAMPTZ NOT NULL,
    count INTEGER NOT NULL,
    PRIMARY KEY (timestamp)
);
