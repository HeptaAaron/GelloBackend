# Gell(o) Backend

Django REST backend for the Gell(o) lab journal app. Gell(o) enables researchers to document, analyze, and manage gel electrophoresis images directly from their smartphone.

Gel images uploaded from the Compose Multiplatform frontend are processed using [GelGenie](https://github.com/mattaq31/GelGenie), an AI-powered segmentation framework. The backend
detects gel bands, counts lanes, and returns structured analysis data alongside the original and processed images.

---

## Tech Stack

- **Python 3.12** (required)
- **Django 6 + Django REST Framework**
- **GelGenie** (U-Net based gel electrophoresis image segmentation)
- **PyTorch** (model inference)
- **PostgreSQL** (database)
- **SimpleJWT** (authentication)

---

## Prerequisites

- Python 3.12 installed
- PostgreSQL running and configured
- Git

---

## Installation

### 1. Clone the repository

```bash
git clone <REPO_URL>
cd GelloBackend
```

### 2. Verify Python version

```bash
python3.12 --version
```

The project strictly requires Python 3.12. Other versions are not supported.

### 3. Set up virtual environment and install dependencies

```bash
make setup
```

This creates a `.venv`, upgrades pip, and installs everything from `requirements.txt`, including GelGenie from GitHub.

### 4. Run database migrations

```bash
make migrate
```

### 5. Start the development server

```bash
make run
```

The server starts at `http://localhost:8000`.

---

## Available Make Commands

| Command        | Description                          |
|----------------|--------------------------------------|
| `make setup`   | Create venv and install dependencies |
| `make run`     | Start Django development server      |
| `make migrate` | Run database migrations              |
| `make shell`   | Open Django interactive shell        |
| `make clean`   | Delete the virtual environment       |

---

## API Endpoints

### Authentication

| Method | Endpoint             | Description               |
|--------|----------------------|---------------------------|
| POST   | `/api/auth/register` | Register a new user       |
| POST   | `/api/auth/login`    | Login, returns JWT tokens |
| POST   | `/api/auth/refresh`  | Refresh access token      |
| POST   | `/api/auth/logout`   | Logout                    |
| GET    | `/api/auth/user`     | Get current user data     |

### Projects

| Method | Endpoint                   | Description       |
|--------|----------------------------|-------------------|
| POST   | `/api/project/create`      | Create a project  |
| GET    | `/api/project`             | List all projects |
| GET    | `/api/project/read/<id>`   | Read a project    |
| PUT    | `/api/project/update/<id>` | Update a project  |
| DELETE | `/api/project/delete/<id>` | Delete a project  |

### Entries

| Method | Endpoint                                      | Description     |
|--------|-----------------------------------------------|-----------------|
| POST   | `/api/project/<project_id>/create`            | Create an entry |
| GET    | `/api/project/<project_id>/`                  | List entries    |
| GET    | `/api/project/<project_id>/read/<entry_id>`   | Read an entry   |
| PUT    | `/api/project/<project_id>/update/<entry_id>` | Update an entry |
| DELETE | `/api/project/<project_id>/delete/<entry_id>` | Delete an entry |

### Gel Analysis

| Method | Endpoint    | Description                     |
|--------|-------------|---------------------------------|
| POST   | `/api/gel/` | Analyze a gel image (see below) |

---

## Gel Analysis Flow

The `/api/gel/` endpoint accepts a gel image and returns structured analysis data. This is a stateless analysis step — nothing is persisted. The frontend later sends the completed
data to the entry API for storage.

### Request

`POST /api/gel/` with `multipart/form-data`:

| Field   | Type | Description                             |
|---------|------|-----------------------------------------|
| `image` | File | Gel image (JPEG, JPG, or PNG supported) |

Requires `Authorization: Bearer <token>` header.

### Response

```json
{
  "image": "<base64 encoded original image>",
  "processed-image": "<base64 encoded segmentation map>",
  "lane-count": 8,
  "table-data": [
    {
      "lane": "A",
      "probe": "",
      "volume": null
    },
    {
      "lane": "B",
      "probe": "",
      "volume": null
    },
    {
      "lane": "C",
      "probe": "",
      "volume": null
    }
  ],
  "note": null
}
```

| Field             | Type          | Description                                                                     |
|-------------------|---------------|---------------------------------------------------------------------------------|
| `image`           | string        | Original image as base64 PNG (as received from the frontend)                    |
| `processed-image` | string        | RGBA segmentation map as base64 PNG (bands highlighted, background transparent) |
| `lane-count`      | number        | Number of detected lanes                                                        |
| `table-data`      | array / null  | One row per lane with empty `probe` and `volume` fields                         |
| `note`            | string / null | Always null from analysis, filled by user in frontend                           |

### Processing Pipeline

1. The uploaded image is converted to RGB, then to grayscale.
2. GelGenie's pretrained U-Net (`universal_finetune`, epoch 590) segments the image — classifying each pixel as either "band" or "background".
3. Connected component analysis (`scipy.ndimage.label`) identifies individual bands.
4. Bands are grouped into vertical lanes based on their horizontal center positions (5% image width tolerance).
5. Lane labels (A, B, C, ...) are assigned left to right.
6. The segmentation map is rendered as an RGBA image: detected bands are colored, the background is transparent.
7. Both images are base64-encoded and returned alongside the lane count and an empty table structure.

### Example (curl)

```bash
# Login
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "your_user", "password": "your_password"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['access'])")

# Analyze gel image
curl -s -X POST http://localhost:8000/api/gel/ \
  -H "Authorization: Bearer $TOKEN" \
  -F "image=@path/to/gel.jpg" | python3 -m json.tool
```

---

## GelGenie Integration

This project uses [GelGenie](https://github.com/mattaq31/GelGenie) (Apache 2.0) for gel band segmentation. The pretrained model weights are downloaded from HuggingFace and stored
in `DjangoBackend/gel_models/`.

GelGenie reference:

> Aquilina, M. et al. "GelGenie: an AI-powered framework for gel electrophoresis image analysis."
> *Nature Communications* 16, 4087 (2025). https://doi.org/10.1038/s41467-025-59189-0

---

## Project Structure

```
GelloBackend/
├── DjangoBackend/
│   ├── gel_models/              # GelGenie pretrained model weights
│   │   └── universal_finetune/
│   ├── processors/
│   │   └── gel_image_processor.py
│   ├── services/
│   │   └── gel_segmentation_service.py
│   ├── views/
│   │   ├── auth_views.py
│   │   ├── entry_views.py
│   │   ├── gel_views.py
│   │   └── project_views.py
│   ├── settings.py
│   └── urls.py
├── Makefile
├── manage.py
├── requirements.txt
└── README.md
```