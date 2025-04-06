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
  ('admin01', 'admin123', 'Anette', 'Tester', 'admin'),
  ('member01', 'member456', 'Mikro', 'Soft', 'member'),
  ('user02', 'user789', 'Tea', 'Time', 'user');
