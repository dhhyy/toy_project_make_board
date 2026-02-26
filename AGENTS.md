# AGENTS.md

## Cursor Cloud specific instructions

### Project overview
Django 3.2.6 hierarchical bulletin board REST API (backend only, no frontend). Two apps: `users` (signup/signin with JWT) and `boards` (CRUD posts with hierarchical replies).

### Local config file
Django settings imports from `my_settings.py` (gitignored). This file must exist at the repo root and export: `SECRET_KEY`, `DATABASES`, `email_validation` (compiled regex), `password_validation` (compiled regex), `algorithm` (JWT algo string). For local dev, configure SQLite:
```python
import re
SECRET_KEY = 'dev-secret-key'
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': 'db.sqlite3'}}
email_validation = re.compile(r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
password_validation = re.compile(r'^[a-zA-Z0-9]{8,}$')
algorithm = 'HS256'
```

### Missing dependencies
`bcrypt`, `PyJWT`, and `freezegun` are imported in code/tests but **not listed in `requirements.txt`**. The update script installs them alongside `requirements.txt`.

### System dependencies
Building `mysqlclient` from `requirements.txt` requires `libmysqlclient-dev`, `pkg-config`, and `python3-dev` system packages (already installed in snapshot).

### Key commands
- **Run tests:** `python3 manage.py test`
- **Run dev server:** `python3 manage.py runserver 0.0.0.0:8000`
- **Run migrations:** `python3 manage.py migrate`

### Gotchas
- The `password_validation` regex in `my_settings.py` requires passwords of 8+ alphanumeric characters. The test suite uses shorter passwords (e.g. `'1234'`, `'12345'`) for signin tests — these work because the validation regex is only applied during signup, not signin.
- Board posts require a `Tag` object to exist (at least `Tag(id=1)`). Create one via shell or tests before posting manually.
- The project uses `APPEND_SLASH = False` — all URL patterns start with `/` after the app prefix (e.g. `/users/signup`, not `/users/signup/`).
