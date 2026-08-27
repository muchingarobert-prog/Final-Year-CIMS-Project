# Deployment Guide

## Production prerequisites

- Python 3.11 or later
- A production database supported by Django, or SQLite on persistent storage for a single-instance deployment
- Persistent storage for `MEDIA_ROOT`
- A web server or platform TLS certificate and HTTPS termination
- A frontend host and backend API host
- SMTP credentials if password-reset email is required

## Required backend environment

Set these variables in the backend runtime. Do not commit a production `.env` file.

```text
DJANGO_SECRET_KEY=<random value of at least 50 characters>
DEBUG=False
ALLOWED_HOSTS=api.example.com
CORS_ALLOWED_ORIGINS=https://app.example.com
CSRF_TRUSTED_ORIGINS=https://app.example.com
SECURE_SSL_REDIRECT=True
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=/persistent/path/db.sqlite3
DEFAULT_FROM_EMAIL=no-reply@example.com
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_HOST_USER=<smtp username>
EMAIL_HOST_PASSWORD=<smtp password>
EMAIL_USE_TLS=True
```

For PostgreSQL, set `DB_ENGINE=django.db.backends.postgresql` and provide `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, and `DB_PORT`.

## Backend deployment

From the repository root:

```bash
python -m venv venv
. venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn cims_project.wsgi:application --bind 0.0.0.0:8000
```

Configure the platform or reverse proxy to forward HTTPS requests to Gunicorn and preserve the `X-Forwarded-Proto: https` header. Serve `/static/` from `STATIC_ROOT` and `/media/` from persistent storage or an object-storage service. Django does not serve media in production mode.

## Frontend deployment

Set the Vite variable before building:

```text
VITE_API_BASE_URL=https://api.example.com
```

Then build the static frontend:

```bash
cd frontend
npm ci
npm run build
```

Serve `frontend/dist` from the frontend host. The development Vite proxy is optional and is not used by the production build.

## Docker

The included Dockerfile runs Gunicorn and is suitable for a container platform. It does not provide persistent database or media storage by itself. Supply the backend environment variables through the platform and attach persistent storage or an external database/media service before using it publicly.

```bash
docker build -t cims-backend .
docker run --env-file .env -p 8000:8000 cims-backend
```

The existing `docker-compose.yml` is for local development and runs Django's development server; it is not the public production deployment definition.

## Release verification

```bash
python manage.py check --deploy
python manage.py makemigrations --check --noinput
python manage.py migrate --check --noinput
python manage.py test
cd frontend
npm run build
```
