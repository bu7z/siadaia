# THIS IS PRE-BRANCH FOR PRODUCTION
_Dont blindly merge Stuff to here otherwise big A-A_

# SIA - Drink and Inventory Advisory

Willkommen zum **SIADaIA**-Projekt!

Dies ist ein Fullstack-Projekt mit einem modernen Vue 3 Frontend (Vite, Bootstrap, Chart.js) und einem Flask-Backend mit PostgreSQL-Anbindung.

_In Planung:_ Einbindung der HASKI-API

## Projekt-Anforderungen

### Node/npm
Mindestens Node 18 wird vorausgesetzt.

> apt max node-v = v12.22.9  
> Lösung:
```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
```
```bash
source ~/.bashrc
```
> Danach installieren:
```bash
nvm install 20
```
```bash
nvm use 20
```
```bash
nvm alias default 20
```

---

### Docker (Compose)

1. Entfernen aller Überbleibsel aus dem Standard-APT-Repo:
```bash
sudo apt-get remove docker docker-engine docker.io containerd runc
```

2. Erforderliche System-Tools:
```bash
sudo apt-get update
```
```bash
sudo apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
```

3. Docker GPG-Key:
```bash
sudo mkdir -p /etc/apt/keyrings
```
```bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
    sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```

4. Docker-Repo (Ubuntu):  
> Wichtig: `ubuntu` ggf. gegen eigene Distro tauschen (z. B. `debian`)  
> https://download.docker.com/linux/ubuntu → https://download.docker.com/linux/debian

```bash
echo \
  "deb [arch=$(dpkg --print-architecture) \
  signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

5. APT-Liste aktualisieren:
```bash
sudo apt-get update
```

6. Docker + Compose aus Docker-Repo installieren:
```bash
sudo apt-get install -y docker-ce docker-ce-cli containerd.io \
    docker-buildx-plugin docker-compose-plugin
```

7. Test:
```bash
docker --version
```
```bash
docker compose version
```

---

## Basic Git

### Neuer Branch

1. Erstellen eines neuen Branches:
```bash
git checkout -b <enter_your_branch_name>
```

2. Staging-Area:
```bash
git add .
```

3. Commit mit eindeutiger Beschreibung:
```bash
git commit -m "https://whatthecommit.com/"
```

4. Erster Push zum Repo:
```bash
git push --set-upstream origin <enter_your_branch_name>
```

4.1 Fortlaufendes Push:
```bash
git push 
```

---

### Mergen eines Branches

1. Wechsel auf `master` (bzw. wohin du mergen willst):
```bash
git checkout master
```

1.1 Aktuellste Änderungen reinholen (optional, aber empfehlenswert):
```bash
git pull origin master
```

2. Merge durchführen:
```bash
git merge <frontend/experimental>
# Enter your branch name you want to merge into "master"
```

> Potenzielle Merge-Konflikte müssen manuell gelöst werden.

3. Push zur Remote (GitHub):
```bash
git push origin master
```

---

### Löschen eines Branches

1. Lokales Löschen des Branches:
```bash
git branch -d <frontend/experimental>
# Enter your branch name you want to delete
```

2. Remote-Löschen des Branches:
```bash
git push origin --delete <frontend/experimental>
# Enter your branch name you want to delete
```

---

### Nice-to-know

#### Synchronisieren einer Datei eines anderen Branches
```bash
git checkout master -- README.md
```
> Kopiert/merged nur die Datei `README.md` in den aktuellen Branch

#### Einrichten eines Alias
```bash
git config --global alias.graph "log --oneline --graph --all --decorate"
```

> Nun lässt sich mit:
```bash
git graph
```

> folgende Ausgabe generieren:
```bash
* eab5672 (HEAD -> master, origin/master, origin/HEAD) Erweiterung README.md - Don’t even try to refactor it.
*   05c3c71 Merge branch 'frontend/experimental' - Derp. Fix missing constant post rename
|\  
| * 05537be (origin/frontend/experimental, frontend/experimental) Landing Page + Login-/RegistrierungsForm - NOJIRA: No cry
| * b7cfa0b minimal MD changes - Pro Tip: Read Copilot output before pushing it
| * 3b4b9e6 Sync README.md from master - more ignores
| * 05bc0d2 Add vue experimentals - Don't Ask Me, I Have No Idea Why This Works Either
* | b8b1ac8 synced back from f/e - more debug... who overwrote!
* | 807c64f Add initial README - Definitely fixing a mistake Copilot made. Totally not mine.
|/  
* 642b4e1 Initial commit - Finished fondling.
```
