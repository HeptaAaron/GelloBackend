# Gell(o) Backend – Installation

## 1. Repository klonen

```
git clone <REPO_URL>
cd GelloBackend
```

---

## 2. Python Version prüfen (Pflicht: 3.12)

```
python3.12 --version
```

---

## 3. Umgebung einrichten (venv + Dependencies)

```
make setup
```

---

## 4. Datenbank Migrationen ausführen

```
make migrate
```

---

## 5. Backend starten

```
make run
```