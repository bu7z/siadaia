# SIA - Drink and Inventory Advisory

Willkommen zum **SIADaIA**-Projekt!

Dies ist ein Fullstack-Projekt mit einem modernen Vue 3 Frontend (Vite, Bootstrap, Chart.js) und einem Flask-Backend mit PostgreSQL-Anbindung.

_In Planung:_ Einbindung HASKI-API


## Projekt-Anforderungen

### Node/npm
mindestens node 18 wir vorrausgesetzt

> apt max node-v = v12.22.9
> Solution:
```
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash

source ~/.bashrc
```
> danach installieren:
```
nvm install 20
nvm use 20
nvm alias default 20
```

### Docker (Compose)

1. Entfernen alle überbleibsel aus standard APT-Repo
```
sudo apt-get remove docker docker-engine docker.io containerd runc
```

2. Erforderliche System-Tools
```
sudo apt-get update
```
```
sudo apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
```

3. Docker GPG-Key
```
sudo mkdir -p /etc/apt/keyrings
```
```
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
    sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```

4. Docker_repo (ubuntu)
> Wichtig: ubuntu gegen eigene distro tauschen (bspw.: debian)
> https://download.docker.com/linux/ubuntu -> https://download.docker.com/linux/debian 
```
echo \
  "deb [arch=$(dpkg --print-architecture) \
  signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```


5. APT-List aktualisieren
```
sudo apt-get update
```

6. Docker + Compose aus docker repo installieren
```
sudo apt-get install -y docker-ce docker-ce-cli containerd.io \
    docker-buildx-plugin docker-compose-plugin
```

7. Test
```
docker --version
```
```
docker compose version
```



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

### Nice-to-know

#### Synchronisieren einer Datei eines anderen Branches
```
git checkout master -- README.md
```
Kopiert/Merged nur die Datei README.md in den aktuellen Branch

#### Einrichten eines alias
```
git config --global alias.graph "log --oneline --graph --all --decorate"
```
> Nun lässt sich mit:

```
git graph
```
> folgende Ausgabe genereiren
```
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
* 642b4e1 Initial commmit - Finished fondling.
```



