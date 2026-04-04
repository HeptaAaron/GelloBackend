# Gell(o) Backend – Benutzer- und Startanleitung

---

## Voraussetzungen

- **Python 3.12** (andere Versionen werden nicht unterstützt)
- **Git**
- **make** (für die bereitgestellten Makefile-Befehle)

---

## Installation

### 1. Repository klonen

```bash
git clone <REPO_URL>
cd GelloBackend
```

### 2. Python-Version prüfen

```bash
python3.12 --version
```

### 3. Virtuelle Umgebung einrichten, Abhängigkeiten installieren und GelGenie-Modell herunterladen

```bash
make setup
```

Dieser Befehl führt folgende Schritte aus:
1. Erstellt eine virtuelle Umgebung (`.venv`)
2. Aktualisiert pip
3. Installiert alle Abhängigkeiten aus `requirements.txt` (inkl. GelGenie direkt von GitHub)
4. Lädt die vortrainierten GelGenie-Modell-Gewichte von HuggingFace herunter nach `DjangoBackend/gel_models/universal_finetune/`

Der Modell-Download ist idempotent – bei erneutem Ausführen werden bereits vorhandene Dateien übersprungen.

---

## Konfiguration

### Datenbank (SQLite)

Die Anwendung verwendet SQLite. Die Datenbankdatei `db.sqlite3` wird automatisch beim ersten Ausführen der Migrationen erstellt. Keine weitere Konfiguration nötig.

### Migrationen ausführen

```bash
make migrate
```

### Admin-Account anlegen

Einen Superuser für die Django-Admin-Oberfläche erstellen:

```bash
.venv/bin/python manage.py createsuperuser
```

Alternativ kann ein normaler Benutzer über den `/api/auth/register`-Endpunkt registriert werden.

---

## Starten der Anwendung

```bash
make run
```

Der Entwicklungsserver startet unter `http://localhost:8000`.

### Kurzanleitung (von Null bis laufend)

```bash
git clone <REPO_URL>
cd GelloBackend
make setup          # venv + deps + GelGenie-Modell
make migrate        # Datenbank erstellen
make run            # Server starten
```

---

## Verfügbare Make-Befehle

| Befehl         | Beschreibung                                                       |
|----------------|--------------------------------------------------------------------|
| `make setup`   | Virtuelle Umgebung erstellen, Abhängigkeiten und Modell installieren |
| `make run`     | Django-Entwicklungsserver starten                                  |
| `make migrate` | Datenbank-Migrationen ausführen                                    |
| `make shell`   | Django-Shell öffnen                                                |
| `make clean`   | Virtuelle Umgebung löschen                                        |

---

## API-Übersicht

Alle Endpunkte sind unter `/api/` erreichbar. Authentifizierte Endpunkte erfordern einen gültigen JWT-Token im Header: `Authorization: Bearer <token>`.

### Authentifizierung

| Methode | Endpunkt              | Beschreibung                                                    |
|---------|-----------------------|-----------------------------------------------------------------|
| POST    | `/api/auth/register`  | Neuen Benutzer registrieren (Username, Passwort)                |
| POST    | `/api/auth/login`     | Einloggen, gibt Access- und Refresh-Token zurück                |
| POST    | `/api/auth/refresh`   | Access-Token mit gültigem Refresh-Token erneuern                |
| POST    | `/api/auth/logout`    | Ausloggen, Refresh-Token wird auf die Blacklist gesetzt         |
| GET     | `/api/auth/user`      | Daten des aktuell eingeloggten Benutzers abrufen                |

### Projekte

| Methode | Endpunkt                        | Beschreibung                                            |
|---------|----------------------------------|---------------------------------------------------------|
| POST    | `/api/project/create`           | Neues Projekt anlegen (Name, Farbe)                     |
| GET     | `/api/project`                  | Alle Projekte des eingeloggten Benutzers auflisten      |
| GET     | `/api/project/read/<id>`        | Einzelnes Projekt anhand der ID abrufen                 |
| PUT     | `/api/project/update/<id>`      | Bestehendes Projekt aktualisieren                       |
| DELETE  | `/api/project/delete/<id>`      | Projekt und zugehörige Einträge löschen                 |

### Einträge

| Methode | Endpunkt                                          | Beschreibung                                        |
|---------|---------------------------------------------------|-----------------------------------------------------|
| POST    | `/api/project/<project_id>/create`                | Neuen Eintrag innerhalb eines Projekts anlegen      |
| GET     | `/api/project/<project_id>/`                      | Alle Einträge eines Projekts auflisten              |
| GET     | `/api/project/<project_id>/read/<entry_id>`       | Einzelnen Eintrag abrufen                           |
| PUT     | `/api/project/<project_id>/update/<entry_id>`     | Bestehenden Eintrag aktualisieren                   |
| DELETE  | `/api/project/<project_id>/delete/<entry_id>`     | Eintrag löschen                                     |

### Gel-Analyse

| Methode | Endpunkt     | Beschreibung                                                                  |
|---------|--------------|-------------------------------------------------------------------------------|
| POST    | `/api/gel/`  | Gel-Bild hochladen und analysieren (zustandslos, speichert nichts)            |

Anfrage als `multipart/form-data` mit Feld `image` (JPEG, JPG oder PNG).

Antwort:

```json
{
  "image": "<Base64 Originalbild>",
  "processed-image": "<Base64 Segmentierungskarte>",
  "lane-count": 5,
  "table-data": [
    { "lane": "A", "probe": "", "volume": null },
    { "lane": "B", "probe": "", "volume": null }
  ],
  "note": null
}
```

---

## Gel-Analyse-Pipeline

Der `/api/gel/`-Endpunkt verarbeitet ein Gel-Bild in folgenden Schritten:

1. Das hochgeladene Bild wird in RGB konvertiert (Originalbild) und anschließend in Graustufen umgewandelt.
2. GelGenie's vortrainiertes U-Net-Modell segmentiert das Bild – jeder Pixel wird als „Bande" oder „Hintergrund" klassifiziert.
3. Connected-Component-Analyse (`scipy.ndimage.label`) identifiziert einzelne Banden.
4. Banden werden anhand ihrer horizontalen Mittelposition in vertikale Lanes gruppiert (Toleranz: 5 % der Bildbreite).
5. Lane-Labels (A, B, C, ...) werden von links nach rechts vergeben.
6. Die Segmentierungskarte wird als RGBA-Bild gerendert (Banden farbig, Hintergrund transparent).
7. Beide Bilder werden Base64-kodiert und zusammen mit Lane-Anzahl und leerer Tabelle als JSON zurückgegeben.

Die Analyse ist zustandslos. Das Frontend sendet das Ergebnis anschließend an die Entry-API zur dauerhaften Speicherung.

---

## Projektstruktur

```
GelloBackend/
├── DjangoBackend/
│   ├── gel_models/              # GelGenie vortrainierte Modell-Gewichte
│   │   └── universal_finetune/
│   ├── models/
│   │   ├── entry_models.py
│   │   └── project_models.py
│   ├── processors/
│   │   └── gel_image_processor.py
│   ├── scripts/
│   │   └── download_models.py   # Modell-Download von HuggingFace
│   ├── services/
│   │   └── gel_segmentation_service.py
│   ├── views/
│   │   ├── auth_views.py
│   │   ├── entry_views.py
│   │   ├── gel_views.py
│   │   └── project_views.py
│   ├── infrastructure/
│   ├── migrations/
│   ├── settings.py
│   └── urls.py
├── docs/
│   ├── project_description.markdown
│   ├── ReadMe.markdown
│   └── presentation.pdf
├── Makefile
├── manage.py
├── requirements.txt
└── README.md
```

---

## Testen mit curl

```bash
# 1. Benutzer registrieren
curl -s -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpassword123"}'

# 2. Einloggen und Token erhalten
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpassword123"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['access'])")

# 3. Gel-Bild analysieren
curl -s -X POST http://localhost:8000/api/gel/ \
  -H "Authorization: Bearer $TOKEN" \
  -F "image=@pfad/zum/gelbild.jpg" | python3 -m json.tool
```

---

## Externe Referenzen

- **GelGenie:** [github.com/mattaq31/GelGenie](https://github.com/mattaq31/GelGenie) (Apache 2.0 Lizenz)
- **GelGenie Paper:** Aquilina, M. et al. „GelGenie: an AI-powered framework for gel electrophoresis image analysis." *Nature Communications* 16, 4087 (2025). [DOI: 10.1038/s41467-025-59189-0](https://doi.org/10.1038/s41467-025-59189-0)