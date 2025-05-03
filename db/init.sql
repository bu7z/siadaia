CREATE TABLE IF NOT EXISTS benutzer (
    id SERIAL PRIMARY KEY,
    benutzername VARCHAR(50) UNIQUE NOT NULL,
    passwort TEXT NOT NULL,
    vorname VARCHAR(100),
    nachname VARCHAR(100),
    rolle VARCHAR(50),
    erstellt_am TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO benutzer (benutzername, passwort, vorname, nachname, rolle)
VALUES 
  ('admin01', '$2b$12$yPNR20SDJ2yTS152PVIvBeO7OWvXBsFJlm42ebfxNub5mAFoCqBk2', 'Anette', 'Tester', 'admin'), -- admin123
  ('member01', '$2b$12$rqR2dbYBvXZyxqjNHrhvNeUgjOU20jPHTEYtQKSC3jSkIdv5z0jyq', 'Mikro', 'Soft', 'member'), -- member456
  ('user02', '$2b$12$nMfWe/.Kc9Khq2iT7.yTRu0kEijE4DnHT4ZXRlUtAf7FwAfE/sbRe', 'Tea', 'Time', 'user');       -- user789



CREATE TABLE IF NOT EXISTS inventar (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    packungseinheit INTEGER NOT NULL,         -- z. B. Anzahl der Flaschen pro Kasten/Paket
    ml_pro_einheit INTEGER NOT NULL,          -- z. B. 700 ml pro Flasche
    ek_preis NUMERIC(10, 2) NOT NULL,         -- Einkaufspreis pro Flasche
    vk_preis NUMERIC(10, 2) NOT NULL,         -- Verkaufspreis
    bild TEXT,                                -- z. B. Pfad oder URL zum Bild (kann NULL sein)
    kategorie VARCHAR(50),                    -- z. B. Biere, Spirituosen, Softdrinks 0,33l
    erstellt_am TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO inventar (name, packungseinheit, ml_pro_einheit, ek_preis, vk_preis, bild, kategorie)
VALUES
  ('Hirsch Helles', 20, 330, 0.87, 2.50, 'hirsch_helles.png', 'Biere'),
  ('Hirsch Zwuckl', 20, 330, 0.87, 2.50, 'hirsch_zwuckl.png', 'Biere'),
  ('Club Mate', 20, 330, 1.12, 2.50, 'club_mate.png', 'Softdrinks 0,33l'),
  ('9 Mile Vodka', 6, 1000, 16.45, 80, 'mile_vodka.png', 'Spirituosen'),
  ('Coca Cola', 12, 1000, 1.32, 2.50, 'coca_cola.png', 'Softdrinks 1l');



CREATE TABLE IF NOT EXISTS inventar_bestand (
    id SERIAL PRIMARY KEY,
    inventar_id INTEGER REFERENCES inventar(id),
    datum TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    anzahl_flaschen INTEGER NOT NULL
);


INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (1, '2025-01-01 19:40:00', 6);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (1, '2025-01-02 15:26:00', 4);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (1, '2025-01-03 19:27:00', 7);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (1, '2025-01-06 10:09:00', 20);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (1, '2025-01-07 20:32:00', 17);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (1, '2025-01-08 08:32:00', 15);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (1, '2025-01-09 09:45:00', 2);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (1, '2025-01-10 18:29:00', 7);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (1, '2025-01-13 17:44:00', 7);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (1, '2025-01-14 15:44:00', 9);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (1, '2025-01-15 12:57:00', 18);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (1, '2025-01-16 14:42:00', 20);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (1, '2025-01-17 09:02:00', 9);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (1, '2025-01-20 15:18:00', 12);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (1, '2025-01-21 16:38:00', 20);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (1, '2025-01-22 12:01:00', 19);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (1, '2025-01-23 17:34:00', 13);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (1, '2025-01-24 15:09:00', 1);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (1, '2025-01-27 16:00:00', 11);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (1, '2025-01-28 12:32:00', 0);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (1, '2025-01-29 19:56:00', 16);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (1, '2025-01-30 16:26:00', 7);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (1, '2025-01-31 12:24:00', 2);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (2, '2025-01-01 12:14:00', 5);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (2, '2025-01-02 14:53:00', 17);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (2, '2025-01-03 13:38:00', 8);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (2, '2025-01-06 10:33:00', 18);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (2, '2025-01-07 18:00:00', 11);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (2, '2025-01-08 09:48:00', 4);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (2, '2025-01-09 14:16:00', 4);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (2, '2025-01-10 09:41:00', 16);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (2, '2025-01-13 13:40:00', 13);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (2, '2025-01-14 15:12:00', 2);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (2, '2025-01-15 15:15:00', 15);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (2, '2025-01-16 13:21:00', 18);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (2, '2025-01-17 15:05:00', 6);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (2, '2025-01-20 08:16:00', 12);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (2, '2025-01-21 13:32:00', 9);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (2, '2025-01-22 20:19:00', 10);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (2, '2025-01-23 12:23:00', 14);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (2, '2025-01-24 13:22:00', 5);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (2, '2025-01-27 09:15:00', 7);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (2, '2025-01-28 18:54:00', 17);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (2, '2025-01-29 11:15:00', 8);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (2, '2025-01-30 10:25:00', 16);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (2, '2025-01-31 12:18:00', 6);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (3, '2025-01-01 19:21:00', 0);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (3, '2025-01-02 19:07:00', 15);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (3, '2025-01-03 17:06:00', 17);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (3, '2025-01-06 09:12:00', 12);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (3, '2025-01-07 20:52:00', 9);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (3, '2025-01-08 11:21:00', 3);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (3, '2025-01-09 10:03:00', 4);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (3, '2025-01-10 08:37:00', 5);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (3, '2025-01-13 09:26:00', 17);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (3, '2025-01-14 12:09:00', 5);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (3, '2025-01-15 13:16:00', 8);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (3, '2025-01-16 11:54:00', 19);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (3, '2025-01-17 17:03:00', 18);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (3, '2025-01-20 17:37:00', 8);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (3, '2025-01-21 10:25:00', 16);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (3, '2025-01-22 15:27:00', 0);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (3, '2025-01-23 12:42:00', 0);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (3, '2025-01-24 14:55:00', 16);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (3, '2025-01-27 10:53:00', 0);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (3, '2025-01-28 11:26:00', 17);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (3, '2025-01-29 20:33:00', 14);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (3, '2025-01-30 17:26:00', 16);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (3, '2025-01-31 09:59:00', 6);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (4, '2025-01-01 09:49:00', 7);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (4, '2025-01-02 14:17:00', 8);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (4, '2025-01-03 13:32:00', 13);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (4, '2025-01-06 15:44:00', 7);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (4, '2025-01-07 18:57:00', 3);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (4, '2025-01-08 18:18:00', 4);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (4, '2025-01-09 20:35:00', 4);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (4, '2025-01-10 14:20:00', 12);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (4, '2025-01-13 18:05:00', 15);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (4, '2025-01-14 14:44:00', 10);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (4, '2025-01-15 20:48:00', 4);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (4, '2025-01-16 18:06:00', 6);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (4, '2025-01-17 16:18:00', 12);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (4, '2025-01-20 17:29:00', 17);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (4, '2025-01-21 18:25:00', 2);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (4, '2025-01-22 09:24:00', 11);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (4, '2025-01-23 20:15:00', 14);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (4, '2025-01-24 18:07:00', 13);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (4, '2025-01-27 13:41:00', 1);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (4, '2025-01-28 13:15:00', 3);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (4, '2025-01-29 13:05:00', 17);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (4, '2025-01-30 15:17:00', 15);
INSERT INTO inventar_bestand (inventar_id, datum, anzahl_flaschen) VALUES (4, '2025-01-31 09:37:00', 10);