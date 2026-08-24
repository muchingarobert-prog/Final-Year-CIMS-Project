# UNZA Congregation Management System

A Django REST API project for managing members, committees, events, attendance, announcements, notifications, documents, visitors, and reports for the New Apostolic Church UNZA Congregation.

## Backend State

The backend is complete for the current project scope and has been validated with the Django test suite.

- All README main API prefixes are implemented.
- Event support uses a single `event_date` timestamp plus recurrence fields.
- The legacy `start_date` / `end_date` fields have been removed.
- The full backend test suite passes with `python manage.py test`.

### Backend Validation Commands

Run the backend validation commands from the project root:

```bash
venv\Scripts\activate
python manage.py test
python manage.py show_urls
```

## Overview

This repository contains the backend for a church management system built with Django and Django REST Framework. It supports user authentication, role-based access, committee management, event tracking, attendance, communications, and reporting workflows.

## Key Features

- Custom user model for church members and staff
- JWT-based authentication and refresh tokens
- Role-aware access for administrators, leaders, and members
- Committee membership and management
- Event and attendance tracking
- Announcements and notifications
- Social and community features for posts, testimonies, and prayer requests
- Reports, finances, documents, and visitor management

## Project Modules

The backend is organized into the following apps:

- accounts
- announcements
- attendance
- audit
- authentication
- church_members
- committees
- dashboard
- documents
- events
- finances
- notifications
- reports
- social
- visitors

## Technology Stack

- Backend: Django 5.2+
- API: Django REST Framework
- Authentication: Simple JWT
- Database: SQLite by default (easy local development)
- Media handling: Django file storage
- CORS support: django-cors-headers

## Prerequisites

- Python 3.10+
- pip
- Virtual environment tool (optional but recommended)

## Installation

1. Clone the repository
```bash
git clone https://github.com/muchingarobert-prog/Final-Year-CIMS-Project.git
cd Final-Year-CIMS-Project
```

2. Create and activate a virtual environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Apply database migrations
```bash
python manage.py migrate
```

5. Create a superuser
```bash
python manage.py createsuperuser
```

6. Run the development server
```bash
python manage.py runserver
```

The API will be available at:
```text
http://127.0.0.1:8000/
```

## React Frontend Demo

A minimal React demo is available under `frontend/`.

The demo uses Vite and React Router to expose several pages:

- `/` - overview
- `/login` - login form
- `/register` - registration form
- `/dashboard` - authenticated dashboard view
- `/committees` - committee list
- `/events` - event list

To run it locally:

```bash
cd frontend
npm install
npm run dev
```

Then open:

```text
http://127.0.0.1:5173/
```

To build the frontend for production:

```bash
npm run build
```

## Main API Routes

The project exposes these main API prefixes:

- /api/auth/ - authentication and token management
- /api/users/ - user and member management
- /api/committees/ - committee operations
- /api/events/ - event and registration endpoints
- /api/attendance/ - attendance tracking
- /api/announcements/ - announcements
- /api/notifications/ - notifications
- /api/social/ - social/community features
- /api/dashboard/ - dashboard data
- /api/reports/ - reports
- /api/finances/ - finance data
- /api/audit/ - audit trails
- /api/documents/ - document management
- /api/visitors/ - visitor management

## Development

Run the backend server:
```bash
python manage.py runserver
```

Run the backend test suite:
```bash
python manage.py test
```

To run just the core API tests added for authentication, committees, events, and dashboard:
```bash
python manage.py test authentication
```

For formatting and linting style, keep the code aligned with the existing Django project conventions and use consistent, readable Python structure.

## Backend API Examples

Register a new user:
```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"newuser","email":"newuser@example.com","password":"Str0ngP@ssw0rd!"}'
```

Log in and retrieve JWT tokens:
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"newuser","password":"Str0ngP@ssw0rd!"}'
```

Get dashboard data (replace TOKEN below):
```bash
curl -H "Authorization: Bearer TOKEN" http://127.0.0.1:8000/api/auth/dashboard/
```

List committees:
```bash
curl -H "Authorization: Bearer TOKEN" http://127.0.0.1:8000/api/committees/
```

List events:
```bash
curl -H "Authorization: Bearer TOKEN" http://127.0.0.1:8000/api/events/
```

## Contributing

1. Create a feature branch
2. Make your changes
3. Add or update tests where appropriate
4. Submit a pull request with a clear summary

## License

This project is intended for internal church administration use. Please confirm licensing terms with the repository owner before redistribution.

## Local Development with Docker

Run the backend quickly with Docker Compose (uses SQLite for local development and an optional Redis service for background tasks):

```bash
docker-compose build
docker-compose up
```

The API will be available at `http://127.0.0.1:8000/`.

## Quick API Examples

List top-level user resource:

```bash
curl -i http://127.0.0.1:8000/api/users/
```

Attempt an unauthenticated request to an auth endpoint:

```bash
curl -i http://127.0.0.1:8000/api/auth/register/
```

Generate an OpenAPI schema locally (requires a Python virtualenv):

```bash
# activate venv first
python manage.py generateschema --format openapi-json --file schema.json
```
