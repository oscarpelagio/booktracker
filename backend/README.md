# Book Tracker API

API REST per a la gestió i seguiment de llibres, amb integració a Google Books API.

## 📝 TODO - Tasques Pendents

### 🔴 Prioritat Alta
1. **Implementar Tests Automatitzats**
   - Tests unitaris per serveis (`pytest`)
   - Tests d'integració per endpoints
   - Mocks per Google Books API
   - Objectiu: >80% coverage

2. **Implementar CI/CD Pipeline**
   - GitHub Actions o GitLab CI
   - Linting amb `ruff` o `black`
   - Type checking amb `mypy`
   - Execució de tests automàtics
   - Build i deploy automàtic

### 🟡 Prioritat Mitjana
3. **Setup Test Infrastructure**
   - Configurar `pytest` amb fixtures
   - Base de dades de test (SQLite o PostgreSQL temporal)
   - Factory patterns per generar dades de test
   - Configuració de conftest.py

4. **Maneig Elegant d'IDs en Respostes**
   - Crear `BookSearchResult` que indiqui font (google/database)
   - Evitar el hack `book_data["id"] = 0`
   - Diferenciar llibres persistits vs no persistits

5. **Setup CI/CD Pipeline**
   - Workflow de GitHub Actions
   - Configurar secrets (GOOGLE_API_KEY, DB credentials)
   - Deploy automàtic a producció

### 🟢 Prioritat Baixa
6. **Mètriques i Observabilitat**
   - Endpoints de Prometheus
   - Structured logging (JSON format)
   - Health checks detallats

7. **Rate Limiting**
   - Protegir APIs externes (Google Books)
   - Límit per usuari/IP

8. **Caching**
   - Redis per cerques freqüents
   - Cache de respostes de Google Books

## 📋 Descripció

Book Tracker és una aplicació backend desenvolupada amb **FastAPI** i **SQLModel** que permet:

- Cercar llibres a través de Google Books API
- Emmagatzemar informació de llibres a una base de dades PostgreSQL
- Gestionar una col·lecció personal de llibres

## 🏗️ Arquitectura

El projecte segueix una arquitectura en capes amb separació de responsabilitats:

```
backend/
├── app/
│   ├── main.py              # Punt d'entrada de l'aplicació
│   ├── core/db.py           # Configuració de la base de dades
│   ├── models/              # Models de dades (SQLModel)
│   ├── crud/                # Capa d'accés a dades (Repository Pattern)
│   ├── services/            # Lògica de negoci
│   ├── clients/             # Clients per APIs externes
│   └── api/v1/              # Endpoints de l'API
└── requirements.txt         # Dependències del projecte
```

### Capes de l'Aplicació

1. **Models** (`app/models/`): Definició d'entitats amb SQLModel
2. **CRUD** (`app/crud/`): Operacions de base de dades (Repository Pattern)
3. **Serveis** (`app/services/`): Lògica de negoci i orquestració
4. **Clients** (`app/clients/`): Integració amb APIs externes (Google Books)
5. **API** (`app/api/v1/`): Endpoints HTTP amb FastAPI

## 🚀 Instal·lació

### Requisits previs

- Python 3.10+
- PostgreSQL
- pip

### Passos d'instal·lació

1. **Clonar el repositori:**
```bash
git clone <repositori>
cd booktracker/backend
```

2. **Crear un entorn virtual:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows
```

3. **Instal·lar dependències:**
```bash
pip install -r requirements.txt
```

4. **Configurar variables d'entorn:**

Crear un fitxer `.env` a la carpeta `backend/` amb el següent contingut:

```env
# Base de dades PostgreSQL
POSTGRES_USER=el_teu_usuari
POSTGRES_PASSWORD=la_teu_contrasenya
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=booktracker

# Google Books API (opcional)
GOOGLE_API_KEY=la_teva_api_key
```

5. **Iniciar l'aplicació:**
```bash
uvicorn app.main:app --reload
```

L'API estarà disponible a: `http://localhost:8000`

## 🐳 Desplegament amb Docker

El projecte inclou un `Makefile` per facilitar la gestió de contenidors Docker.

### Comandes disponibles

| Comanda | Descripció |
|---------|------------|
| `make env` | Copia `.env.example` a `.env` |
| `make build` | Construeix i inicia els contenidors (`docker compose up -d --build`) |
| `make up` | Inicia els contenidors existents (`docker compose up -d`) |
| `make down` | Atura i elimina els contenidors (`docker compose down`) |

### Desplegament ràpid

```bash
# 1. Configurar variables d'entorn
make env
# Edita el fitxer .env amb les teves credencials

# 2. Construir i iniciar els serveis
make build

# 3. L'API estarà disponible a: http://localhost:8000
```

### Aturar els serveis

```bash
make down
```

### Desplegament manual (sense Make)

Si prefereixes no utilitzar `make`:

```bash
# Configurar variables d'entorn
cp .env.example .env

# Construir i iniciar
docker compose up -d --build

# Aturar
docker compose down
```

## 📖 Documentació de l'API

Un cop iniciat el servidor, pots accedir a:

- **Documentació interactiva (Swagger UI):** `http://localhost:8000/docs`
- **Documentació alternativa (ReDoc):** `http://localhost:8000/redoc`

## 🔌 Endpoints

### Health Check
```http
GET /
```
Retorna l'estat del servidor.

### Cercar llibres per títol
```http
GET /api/v1/google/search-by-title?title={titol_del_llibre}
```

Cerca un llibre a Google Books i el guarda automàticament a la base de dades si té ISBN.

**Paràmetres:**
- `title` (obligatori): Títol del llibre a cercar

**Resposta:**
```json
{
  "id": 1,
  "title": "El nom del llibre",
  "author": "Nom de l'autor",
  "publisher": "Editorial",
  "publisher_date": "2023-01-01",
  "description": "Descripció del llibre",
  "isbn": "9781234567890",
  "page_count": 300,
  "print_type": "BOOK",
  "categories": "Ficció, Novel·la",
  "maturity_rating": "NOT_MATURE",
  "small_thumbnail": "url_imatge_petita",
  "thumbnail": "url_imatge",
  "language": "ca",
  "preview_link": "url_previsualitzacio"
}
```

## 🔧 Variables d'Entorn

| Variable | Descripció | Obligatori | Per defecte |
|----------|------------|------------|-------------|
| `POSTGRES_USER` | Usuari de PostgreSQL | Sí | - |
| `POSTGRES_PASSWORD` | Contrasenya de PostgreSQL | Sí | - |
| `POSTGRES_HOST` | Host de la base de dades | No | `db` |
| `POSTGRES_PORT` | Port de PostgreSQL | No | `5432` |
| `POSTGRES_DB` | Nom de la base de dades | Sí | - |
| `GOOGLE_API_KEY` | API Key de Google Books | No | - |

## ✨ Millores Recents

### 1. HTTP Client Singleton (GoogleBooksClient)
**Implementat**: Patró Singleton per al client de Google Books
- **Benefici**: Reuse de connexions HTTP, millor rendiment
- **Característiques**:
  - Una sola instància del client HTTP amb `httpx.AsyncClient`
  - Límits de connexió configurats (max 10 connexions)
  - Timeout de 30 segons
  - Mètode `close()` per tancar connexions de forma segura
  - Factory function `get_google_books_client()` amb cache

```python
# Ús amb dependency injection
from app.clients import get_google_books_client

client = get_google_books_client()  # Retorna instància cachejada
```

### 2. Validació Estricta de Dades Externes
**Implementat**: Validació robusta de les dades de Google Books
- **Benefici**: Maneig segur de dades inconsistents
- **Característiques**:
  - Mètodes helpers per extracció segura de dades
  - Normalització d'autors i categories
  - Parseig flexible de dates (YYYY, YYYY-MM, YYYY-MM-DD)
  - Valors per defecte per camps obligatoris
  - Extracció d'ISBN amb prioritat (ISBN_13 > ISBN_10)

```python
# Exemple de mètodes de validació
_extract_isbn(identifiers)      # Extracció segura d'ISBN
_parse_date(date_str)           # Parseig flexible de dates
_normalize_list(data)           # Normalització de llistes
_safe_get_string(data, key)     # Accés segur a diccionaris
_safe_get_nested(data, keys)    # Accés segur a diccionaris niats
```

## 🗄️ Migracions de Base de Dades (Alembic)

El projecte utilitza **Alembic** per gestionar les migracions de la base de dades.

### Comandes disponibles (Makefile)

| Comanda | Descripció |
|---------|------------|
| `make migrate` | Aplica totes les migracions pendents (`alembic upgrade head`) |
| `make migration` | Crea una nova migració (`alembic revision --autogenerate`) |
| `make downgrade` | Reverteix migracions (`alembic downgrade`) |
| `make migration-history` | Mostra l'historial de migracions |
| `make current-migration` | Mostra la migració actual |

### Ús bàsic

**Crear una nova migració (després de modificar models):**
```bash
make migration
# Introdueix el nom de la migració quan et demani
```

**Aplicar migracions a la base de dades:**
```bash
make migrate
```

**Veure migració actual:**
```bash
make current-migration
```

**Reverter l'última migració:**
```bash
make downgrade
# Introdueix "-1" per revertir una migració
```

### Estructura de Migracions

Les migracions es guarden a `backend/alembic/versions/` amb el format:
```
YYYY_MM_DD_HHMM-<hash>_<nom_de_la_migracio>.py
```

### Configuració

- **alembic.ini**: Configuració general d'Alembic
- **alembic/env.py**: Configuració de connexió i metadades (utilitza variables d'entorn)
- **SQLModel**: Els models es carreguen automàticament des de `app.models`

## 🧪 Tecnologies Utilitzades

- **FastAPI**: Framework web modern i ràpid
- **SQLModel**: ORM basat en SQLAlchemy i Pydantic
- **PostgreSQL**: Base de dades relacional
- **Alembic**: Gestió de migracions de base de dades
- **Pydantic**: Validació de dades
- **HTTPX**: Client HTTP asíncron

## 📁 Estructura del Projecte

```
booktracker/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # Aplicació FastAPI
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   └── db.py              # Configuració PostgreSQL
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── book.py            # Models de base de dades
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   └── book.py            # Esquemes Pydantic per API
│   │   ├── crud/
│   │   │   ├── __init__.py
│   │   │   └── book_repository.py # Operacions CRUD
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   └── book_service.py    # Lògica de negoci
│   │   ├── clients/
│   │   │   ├── __init__.py
│   │   │   └── google_client.py   # Client Google Books
│   │   └── api/
│   │       ├── __init__.py
│   │       └── v1/
│   │           ├── __init__.py
│   │           ├── router.py       # Rutes principals
│   │           └── endpoints/
│   │               ├── __init__.py
│   │               └── google.py   # Endpoints Google
│   ├── alembic/                    # Configuració d'Alembic
│   │   ├── env.py                  # Configuració de migracions
│   │   ├── versions/               # Fitxers de migració
│   │   └── README.md
│   ├── alembic.ini                 # Configuració d'Alembic
│   ├── requirements.txt
│   └── .env                        # Variables d'entorn (no incloure al git)
├── docker-compose.yaml
├── Dockerfile
├── Makefile
└── .env.example
```

## 🤝 Contribucions

Les contribucions són benvingudes! Si vols contribuir:

1. Fes un fork del repositori
2. Crea una branca per la teva funcionalitat (`git checkout -b feature/nova-funcionalitat`)
3. Fes commit dels canvis (`git commit -am 'Afegir nova funcionalitat'`)
4. Fes push a la branca (`git push origin feature/nova-funcionalitat`)
5. Obre una Pull Request

## 📝 Llicència

Aquest projecte està sota la llicència MIT.

## 👤 Autor

Desenvolupat amb ❤️ per l'equip de Book Tracker.