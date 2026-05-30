# FastAPI Notes API

A production-style REST API built with **FastAPI**, featuring JWT authentication, SQLAlchemy ORM persistence, per-user data isolation, and a clean layered architecture. Two resource domains — **notes** and **books** — share a single authentication system.

This project was built lesson-by-lesson as a deep dive into idiomatic, scalable FastAPI development: not just "make it work," but "make it the way a team would actually ship it."

---

## Features

- **JWT authentication** — register, log in, and receive a signed token (bcrypt-hashed passwords; plaintext is never stored).
- **Per-user data isolation** — every note and book belongs to a user; you can only see and modify your own data.
- **Full CRUD** — create, read, update, and delete for both notes and books.
- **Filtering & pagination** — list endpoints support search, range filters, and `skip` / `limit` pagination.
- **Layered architecture** — HTTP, persistence, database models, and validation schemas are cleanly separated.
- **Automatic interactive docs** — Swagger UI at `/docs` and ReDoc at `/redoc`, generated from the code.
- **Self-documenting validation** — Pydantic models validate every request and shape every response.

---

## Tech Stack

| Layer | Tool |
|---|---|
| Web framework | FastAPI |
| Validation | Pydantic v2 |
| ORM | SQLAlchemy |
| Database | SQLite (swappable for PostgreSQL) |
| Auth | JWT (python-jose) + bcrypt |
| Server | Uvicorn |

---

## Project Structure

```
.
├── main.py              # App entry point: middleware, routers, health check
├── database.py          # Shared engine, session factory, and get_db dependency
├── users/               # Authentication domain
│   ├── models.py        # User SQLAlchemy model
│   ├── schemas.py       # UserCreate, UserResponse, Token
│   ├── security.py      # Hashing, JWT, get_current_user dependency
│   ├── storage.py       # User persistence
│   └── router.py        # /auth/register, /auth/login
├── notes/               # Notes domain
│   ├── models.py        # Note SQLAlchemy model
│   ├── schemas.py       # NoteCreate, NoteResponse
│   ├── storage.py       # Note persistence (pure functions)
│   └── router.py        # /notes endpoints
└── books/               # Books domain
    ├── models.py
    ├── schemas.py
    ├── storage.py
    └── router.py
```

**Design principle:** routers handle HTTP, storage handles persistence, models map to the database, and schemas define the request/response contracts. Each layer changes for one reason.

---

## Getting Started

### Prerequisites

- Python 3.10+ (developed on 3.14)

### Installation

```bash
# Clone the repo
git clone https://github.com/<!-- TODO: your-username -->/fastapi-notes-api.git
cd fastapi-notes-api

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running

```bash
fastapi dev main.py
```

The API will be available at `http://127.0.0.1:8000`.

- Interactive docs (Swagger UI): `http://127.0.0.1:8000/docs`
- Alternative docs (ReDoc): `http://127.0.0.1:8000/redoc`

---

## Usage

### 1. Register a user

```bash
curl -X POST http://127.0.0.1:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice", "email": "alice@example.com", "password": "supersecret"}'
```

### 2. Log in to get a token

```bash
curl -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=alice@example.com&password=supersecret"
```

Returns:

```json
{ "access_token": "eyJhbGci...", "token_type": "bearer" }
```

### 3. Create a note (authenticated)

```bash
curl -X POST http://127.0.0.1:8000/notes \
  -H "Authorization: Bearer <your-token>" \
  -H "Content-Type: application/json" \
  -d '{"title": "First note", "content": "Hello, FastAPI!"}'
```

> **Tip:** The easiest way to explore is `/docs` — click **Authorize**, enter your email and password, and the interactive UI handles the token for you.

---

## API Reference

### Auth

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| `POST` | `/auth/register` | Create a new user account | No |
| `POST` | `/auth/login` | Log in, receive a JWT | No |

### Notes

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| `GET` | `/notes` | List your notes (`?title=`, `?archived=`, `?skip=`, `?limit=`) | Yes |
| `POST` | `/notes` | Create a note | Yes |
| `GET` | `/notes/{id}` | Get one of your notes | Yes |
| `PUT` | `/notes/{id}` | Update one of your notes | Yes |
| `PATCH` | `/notes/{id}` | Toggle a note's archived status | Yes |
| `DELETE` | `/notes/{id}` | Delete one of your notes | Yes |

### Books

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| `GET` | `/books` | List books (`?author=`, `?year_from=`, `?year_to=`, `?skip=`, `?limit=`) | No |
| `POST` | `/books` | Create a book | Yes |
| `GET` | `/books/{id}` | Get one book | No |
| `PUT` | `/books/{id}` | Update a book (owner only) | Yes |
| `DELETE` | `/books/{id}` | Delete a book (owner only) | Yes |

> Accessing a note that isn't yours returns **404** (not 403) — the API does not reveal whether other users' notes exist.

---

## Security Notes

- Passwords are hashed with **bcrypt** (per-password salt); plaintext is never stored or returned.
- Authentication uses signed **JWT** tokens with expiry.
- Login and not-found responses are deliberately vague to avoid **user enumeration**.
- The `SECRET_KEY` in this repo is a development placeholder. In production it must be loaded from an environment variable and never committed.

---

## Roadmap

- [ ] Automated test suite (pytest + TestClient)
- [ ] Environment-based configuration (`.env`)
- [ ] Database migrations (Alembic)
- [ ] PostgreSQL support
- [ ] Dockerized deployment
- [ ] Role-based / policy-based authorization (admin override)

---

## License

<!-- TODO: choose a license, e.g. MIT. You can add one via GitHub's "Add file" → "Create new file" → name it LICENSE, and GitHub offers templates. -->

This project is licensed under the MIT License.

---

## Acknowledgments

Built as a structured, hands-on learning project covering FastAPI from first endpoint to production-style architecture.
