<div align="center">

# 🫧 FocusBubble Backend

### Android Productivity and Digital Wellbeing Application

### Kotlin + Jetpack Compose Focus Session Application with App Blocking

<br/>

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Uvicorn](https://img.shields.io/badge/Uvicorn-ASGI-20232A?style=for-the-badge)](https://www.uvicorn.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge)](https://www.sqlalchemy.org/)
[![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=for-the-badge)](https://docs.pydantic.dev/)
[![Render](https://img.shields.io/badge/Render-Deployment-46E3B7?style=for-the-badge&logo=render&logoColor=black)](https://render.com/)
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)

</div>

---

# 📑 Table of Contents

- [Overview](#overview)
- [Backend Responsibilities](#backend-responsibilities)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Frontend Integration](#frontend-integration)
- [Database Architecture](#database-architecture)
- [API Workflow](#api-workflow)
- [Getting Started](#getting-started)
- [Local Development](#local-development)
- [Render Deployment](#render-deployment)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Security](#security)
- [Demo](#demo)
- [Author](#author)

---

<a id="overview"></a>

# 🔍 Overview

FocusBubble is an Android productivity and digital-wellbeing application that helps users block distracting applications during timed focus sessions.

This repository contains the backend API for the FocusBubble Android application.

The backend provides REST APIs for:

- Authentication support.
- User management.
- Focus-session creation.
- Session pause/resume/stop operations.
- Schedule management.
- Block synchronization.
- Session history.
- Database persistence.

The Android frontend communicates with this backend through Retrofit and OkHttp.

---

<a id="backend-responsibilities"></a>

# 🌐 Backend Responsibilities

The backend is responsible for:

- Validating API requests.
- Managing users.
- Creating focus sessions.
- Updating session state.
- Managing schedules.
- Managing blocked applications.
- Saving session history.
- Returning structured JSON responses.
- Connecting to the hosted relational database.
- Providing API documentation through FastAPI Swagger UI.

The Android application remains responsible for real-time blocking and AccessibilityService enforcement.

---

<a id="architecture"></a>

# 🏗️ Architecture

```text
┌──────────────────────────────────────────────┐
│              FocusBubble Android App         │
│                                              │
│  Kotlin + Jetpack Compose                    │
│  Room + Retrofit                              │
└──────────────────────┬───────────────────────┘
                       │
                       │ HTTPS REST API
                       ▼
┌──────────────────────────────────────────────┐
│              FastAPI Backend                 │
│                                              │
│  main.py                                     │
│  auth.py                                     │
│  crud.py                                     │
│  schemas.py                                  │
│  models.py                                   │
│  database.py                                 │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│          Hosted Relational Database          │
└──────────────────────────────────────────────┘
```

## Backend Request Flow

```text
Android Retrofit Request
        ↓
FastAPI Route
        ↓
Pydantic Schema Validation
        ↓
Authentication/Authorization
        ↓
CRUD Function
        ↓
SQLAlchemy Model
        ↓
Relational Database
        ↓
JSON Response
```

---

<a id="technology-stack"></a>

# 🛠️ Technology Stack

| Category | Technology | Purpose |
|---|---|---|
| Language | Python | Backend implementation |
| Framework | FastAPI | REST API |
| ASGI Server | Uvicorn | Local and production server |
| ORM | SQLAlchemy | Database access |
| Validation | Pydantic | Request/response models |
| Authentication | Custom auth/Firebase integration | Identity and access |
| Database | Hosted relational database | Persistent data |
| Hosting | Render | Backend deployment |
| Documentation | FastAPI Swagger/OpenAPI | API testing |
| Version Control | Git/GitHub | Source management |

---

<a id="project-structure"></a>

# 📁 Project Structure

```text
Focusbubble-Backend/
├── __init__.py
├── auth.py
├── background.py
├── crud.py
├── database.py
├── main.py
├── models.py
├── requirements.txt
├── .gitignore
└── README.md
```

## File Responsibilities

### `main.py`

Contains:

- FastAPI application creation.
- API routes.
- Dependency injection for database sessions.
- Request handling.
- Response handling.
- Application startup logic.

### `auth.py`

Contains authentication-related functionality such as:

- User identity validation.
- Authentication helpers.
- Token or identity integration.
- User lookup support.

### `background.py`

Contains background/session-related logic used by the backend.

### `crud.py`

Contains database operations such as:

- User queries.
- Session creation.
- Session pause/resume/stop.
- Blocked-app creation.
- Schedule operations.
- History operations.

### `database.py`

Contains:

- Database engine creation.
- SQLAlchemy `Base`.
- Database session factory.
- `get_db` dependency.
- Database URL configuration.

### `models.py`

Contains SQLAlchemy model classes and table definitions.

### `schemas.py`

Contains Pydantic models for:

- Request validation.
- Response serialization.
- Session data.
- User data.
- Schedule data.
- Blocked-app data.

### `requirements.txt`

Contains Python dependencies required by the backend.

---

<a id="frontend-integration"></a>

# 🔗 Frontend Integration

Frontend repository:

```text
Focusbubble-Frontend
```

Backend repository:

```text
[https://github.com/rozanaim2026/Focusbubble-Backend](https://github.com/rozanaim2026/Focusbubble-Backend)
```

Android integration files:

```text
data/network/FocusBubbleApi.kt
data/network/RetrofitClient.kt
data/model/ApiModels.kt
data/repository/UserRepository.kt
data/repository/SessionRepository.kt
data/repository/ScheduleRepository.kt
data/repository/BlockedAppsRepository.kt
```

## Production Base URL

```text
[https://your-render-service.onrender.com/]
```

The Android Retrofit base URL must end with `/`.

## Example Session Request

```http
POST /users/{user_id}/sessions
Content-Type: application/json
```

```json
{
  "duration_minutes": 25,
  "user_id": 24
}
```

## Example Session Routes

```text
POST /users/{user_id}/sessions
POST /sessions/{session_id}/pause
POST /sessions/{session_id}/resume
POST /sessions/{session_id}/stop
```

The exact routes should be confirmed in `main.py` and the Swagger documentation.

---

<a id="database-architecture"></a>

# 🗄️ Database Architecture

The backend stores shared application data in a relational database.

Typical logical tables include:

```text
users
sessions
schedules
blocked_apps
session_apps
session_history
```

## SQLAlchemy Model Rule

The table name in a foreign key must match the target model’s `__tablename__`.

Correct:

```python
class BlockedApp(Base):
    __tablename__ = "blocked_apps"
```

```python
app_id = Column(
    Integer,
    ForeignKey("blocked_apps.id")
)
```

Incorrect unless an `apps` table exists:

```python
ForeignKey("apps.id")
```

## Model Import Rule

All models must be imported before:

```python
Base.metadata.create_all(bind=engine)
```

Otherwise SQLAlchemy may report:

```text
NoReferencedTableError
```

## Inspect Registered Tables

Run from the backend root:

```bash
python -c \
"from main import Base; print(list(Base.metadata.tables.keys()))"
```

Expected output should contain the tables used by your foreign keys.

---

<a id="api-workflow"></a>

# 🔄 API Workflow

## Create Session

```text
Android sends request
        ↓
FastAPI receives request
        ↓
Pydantic validates body
        ↓
User is checked
        ↓
Session is inserted
        ↓
Response is returned
        ↓
Android starts local enforcement
```

## Stop Session

```text
Android sends stop request
        ↓
Backend updates session status
        ↓
History/statistics are recorded
        ↓
Android stops services and removes overlays
```

## Backend and Local Enforcement

The Android application should not depend completely on the backend to block apps.

The Android app uses:

- Room for immediate local blocked-app lookups.
- AccessibilityService for foreground detection.
- BlockOverlayService for enforcement.

The backend is used for:

- Shared user/session data.
- Session history.
- Schedules.
- Synchronization.
- Remote reporting.

---

<a id="getting-started"></a>

# 🚀 Getting Started

## Clone the Repository

```bash
git clone [https://github.com/rozanaim2026/Focusbubble-Backend.git]
cd Focusbubble-Backend
```

## Verify Files

```bash
ls
```

You should see:

```text
auth.py
background.py
crud.py
database.py
main.py
models.py
schemas.py
requirements.txt
```

---

<a id="local-development"></a>

# 💻 Local Development

## Create a Virtual Environment

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

## Upgrade pip

```bash
python -m pip install --upgrade pip
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Configure Environment Variables

Create a local `.env` file using the variables required by `database.py` and `auth.py`.

Example:

```env
DATABASE_URL=your_database_url
SECRET_KEY=your_secret_key
CORS_ORIGINS=your_allowed_origins
```

Do not commit `.env`.

## Run FastAPI

```bash
uvicorn main:app \
    --reload \
    --host 127.0.0.1 \
    --port 8000
```

## Open Swagger UI

```text
http://127.0.0.1:8000/docs
```

## Open ReDoc

```text
http://127.0.0.1:8000/redoc
```

## Validate Syntax

```bash
python -m py_compile main.py
```

## Inspect Routes

```bash
python -c \
"from main import app; print(app.routes)"
```

---

<a id="render-deployment"></a>

# ☁️ Render Deployment

## Create the Web Service

1. Open the Render Dashboard.
2. Click **New**.
3. Select **Web Service**.
4. Connect the GitHub repository.
5. Select the backend branch.
6. Choose Python runtime.
7. Add build and start commands.
8. Add environment variables.
9. Deploy the service.

## Build Command

```bash
pip install -r requirements.txt
```

## Start Command

```bash
uvicorn main:app \
    --host 0.0.0.0 \
    --port $PORT
```

Render’s FastAPI deployment guide uses this deployment pattern. [264]

## Environment Variables

Add environment variables from:

```text
Render Dashboard
→ FocusBubble Backend Service
→ Environment
```

Typical values:

```text
DATABASE_URL
SECRET_KEY
CORS_ORIGINS
```

Never commit real credentials to GitHub.

## Verify Deployment

```text
[https://your-service.onrender.com/](https://your-service.onrender.com/)
[https://your-service.onrender.com/docs](https://your-service.onrender.com/docs)
```

## Render Logs

Check Render logs for:

- Python import errors.
- Indentation errors.
- Missing dependencies.
- Database connection failures.
- SQLAlchemy model errors.
- Port binding failures.
- User/session API errors.

---

<a id="testing"></a>

# ✅ Testing

## Syntax Test

```bash
python -m py_compile main.py
```

## Local API Test

```bash
curl http://127.0.0.1:8000/
```

## Swagger Test

Open:

```text
http://127.0.0.1:8000/docs
```

Test:

- User creation or lookup.
- Session creation.
- Session pause.
- Session resume.
- Session stop.
- Schedule operations.
- Block synchronization.

## Android Integration Test

1. Start the backend locally or deploy it to Render.
2. Configure `RetrofitClient.kt`.
3. Launch the Android app.
4. Sign in.
5. Create or load the user.
6. Start a focus session.
7. Inspect OkHttp logs.
8. Confirm the session appears in the backend database.

## Expected OkHttp Logging

```text
--> POST [https://your-service.onrender.com/users/24/sessions](https://your-service.onrender.com/users/24/sessions)
<-- 200 [https://your-service.onrender.com/users/24/sessions](https://your-service.onrender.com/users/24/sessions)
```

---

<a id="troubleshooting"></a>

# 🛠️ Troubleshooting

## `IndentationError`

Run:

```bash
python -m py_compile main.py
```

Inspect the reported line and the surrounding block.

## `NoReferencedTableError`

Check:

```python
ForeignKey("blocked_apps.id")
```

matches:

```python
__tablename__ = "blocked_apps"
```

Also verify that the model is imported before metadata creation.

## `ModuleNotFoundError`

Install dependencies:

```bash
pip install -r requirements.txt
```

Check that imports match the actual file names.

## `User not found`

A response such as:

```json
{
  "detail": "User not found"
}
```

means:

- The backend route was reached.
- The requested user ID is absent in the connected database.
- Android connectivity is working.
- The database environment may not be the one expected.

## Render Port Failure

Use:

```bash
uvicorn main:app \
    --host 0.0.0.0 \
    --port $PORT
```

Do not hard-code a production port.

## Database Connection Failure

Check:

- `DATABASE_URL`.
- Database availability.
- SSL requirements.
- Render environment variables.
- Database network access.
- SQLAlchemy engine configuration.

---

<a id="security"></a>

# 🔐 Security

- Never commit `.env`.
- Never expose database passwords.
- Never log authentication tokens.
- Validate user ownership for every session route.
- Do not trust client-supplied `user_id` without authorization.
- Use HTTPS in production.
- Configure CORS carefully.
- Use database migrations for schema changes.
- Rotate secrets if they are exposed.
- Separate development, staging, and production databases.

---

<a id="demo"></a>

# 🎥 Demo

A screen recording of the FocusBubble application will be added here.

```text
Demo video:
[Add Google Drive link here]
```

Example:

```markdown
[▶️ Watch FocusBubble Demo](YOUR_GOOGLE_DRIVE_LINK_HERE)
```

---

<a id="author"></a>

# 👩‍💻 Author

<div align="center">

## Rozana IM

Android Developer • Backend Developer • Cloud and DevOps Enthusiast

GitHub: [https://github.com/rozanaim2026](https://github.com/rozanaim2026)

Frontend Repository:

[FocusBubble Frontend](YOUR_FRONTEND_REPOSITORY_LINK_HERE)

Backend Repository:

[FocusBubble Backend](https://github.com/rozanaim2026/Focusbubble-Backend)

</div>

---

# ⭐ Support

If you found this project useful, please consider giving the repository a ⭐ on GitHub.

<div align="center">

### Built with Kotlin • Jetpack Compose • Room • Retrofit • FastAPI • SQLAlchemy • Render

</div>
