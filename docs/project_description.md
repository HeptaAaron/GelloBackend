# Dokumentation zur Projektarbeit im Wahlpflichtkurs Django

**Projektname:** Gell(o)
**Projektart:** Compose Multiplatform Applikation (mobile-first) mit Django REST API Backend
**Projektteam:** Fabian Brüns, Aaron Pieperjohann, Manuel Gilles

---

## Kurzbeschreibung

Gell(o) ist eine mobile-first Labor-Tagebuch-Anwendung, die es ermöglicht, digitale Tagebücher anzulegen und darin strukturierte Einträge zu erfassen. Ziel des Projekts ist es, klassische Laborbücher durch eine moderne, digitale Lösung zu ersetzen, die insbesondere für die Dokumentation von Experimenten mit Gelbildern geeignet ist.

Ein Nutzer kann mehrere Tagebücher (Projekte) erstellen, diese benennen und farblich kennzeichnen. Innerhalb eines Projekts lassen sich Einträge mit unterschiedlichen Typen anlegen, darunter Notizen, Protokolle und Gel-Einträge.

Ein besonderer Fokus liegt auf Gel-Einträgen: Beim Erstellen eines Gel-Eintrags wird ein Bild hochgeladen und serverseitig mithilfe von GelGenie analysiert. GelGenie ist ein KI-gestütztes Open-Source-Framework der Universität Edinburgh, das auf einem U-Net-Modell basiert und Gel-Elektrophorese-Bilder automatisch segmentiert. Die erkannten Banden werden in Lanes gruppiert, in einer Tabelle dargestellt und können vom Benutzer manuell überprüft und ergänzt werden (Probenbezeichnung, Volumen, Notizen).

Die Anwendung ist modular aufgebaut und trennt Frontend und Backend klar voneinander. Die Kommunikation erfolgt ausschließlich über eine REST-API. Die Entwicklung erfolgt iterativ mit einem Kanban-Workflow.

---

## Technische Umsetzung

| Komponente           | Technologie                                              |
|----------------------|----------------------------------------------------------|
| Frontend             | Compose Multiplatform (mobile-first, Android + iOS)      |
| Backend              | Python 3.12, Django 6, Django REST Framework             |
| Datenbank            | SQLite (dateibasiert, keine Konfiguration nötig)         |
| Authentifizierung    | SimpleJWT (Access- und Refresh-Tokens)                   |
| Gel-Analyse          | GelGenie (U-Net Segmentierung), PyTorch, SciPy           |
| Versionsverwaltung   | Git (getrennte Repositories für Frontend und Backend)     |
| Projektmanagement    | Kanban mit YouTrack                                      |
| Testumgebung         | Android (Google Pixel Testgerät), iOS                    |

---

## Must-Have-Funktionen

- **Projekt-Ordner-Struktur:** Projekte können angelegt, benannt und durch Farbe gekennzeichnet werden.
- **Einträge innerhalb von Projekten:** Einträge mit Datum und Art (Gel, Notiz, Protokoll etc.) anlegen. Jede Art hat ein eigenes Icon.
- **Gel-Templates:** Der Benutzer kann das Gel-Template (Bild und Tabelle) in einem Editor bearbeiten und als Gel-Art speichern.
- **Gel-Bild-Upload und Analyse:** Nach dem Upload wird das Bild automatisch ausgewertet. Die Analyse erkennt Lanes und Banden, stellt die Ergebnisse als Bild und Tabelle dar. Der Benutzer entscheidet, ob Bild, Tabelle oder beides übernommen werden soll.
- **Manuelle Nachbearbeitung:** Der Benutzer überprüft die erkannten Werte in der Tabelle und passt sie manuell an (Probenbezeichnung, Volumen).
- **Benutzerauthentifizierung:** Registrierung, Login, Logout mit JWT-basierter Authentifizierung.

---

## Nice-to-Have-Funktionen

- Bild-Vorverarbeitung im Frontend (Begradigung, Helligkeitsanpassung)
- Export von Einträgen als PDF
- Suchfunktion über alle Projekte und Einträge

---

## Nicht-Ziele

- Keine Desktop-Anwendung – die App ist ausschließlich für Smartphones konzipiert.
- Kein eigenes Training von KI-Modellen – es werden ausschließlich vortrainierte GelGenie-Modelle verwendet.
- Keine Echtzeit-Kollaboration zwischen mehreren Nutzern.
- Keine Anbindung an externe Laborgeräte oder LIMS-Systeme.