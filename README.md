# SIA - Drink and Inventory Advisory

Willkommen zum **SIADaIA**-Projekt!

Dies ist ein Fullstack-Projekt mit einem modernen Vue 3 Frontend (Vite, Bootstrap, Chart.js) und einem Flask-Backend mit PostgreSQL-Anbindung.

_In Planung:_ Einbindung HASKI-API

## Basic Git


### Neuer Branch


1. Erstellen eines neuen Branches
```
git checkout -b <enter_your_branch_name>
```

2. Staging-Area 
```
git add .
```

3. Commiten mit eindeutiger Beschreibung
```
git commit -m "https://whatthecommit.com/"
```

4. erster push zum Repo
```
git push --set-upstream origin <enter_your_branch_name>
```

4.1 fortlaufendes push
```
git push 
```

### Mergen eines Branches


1. Wechsel auf master (bzw. wohin du mergen wills)
```
git checkout master
```

1.1 Aktuellste Änderungen reinholen (optional, aber empfehlenswert)

```
git pull origin master
```

2. Merge durchführen
```
git merge <frontend/experimental>
# enter your branch name you want to mergen into "master"
```
potentielle Merge-Koflikte müssen manuell gelöst werden.

3. Push zur Remote (GitHub)
```
git push origin master
```

### Löschen eines Branch

1. Lokales Löschen der Branches
```
git branch -d frontend/experimental
# enter your branch name you want to delete
```

2. Remote löschen des Branches
```
git push origin --delete frontend/experimental
```

