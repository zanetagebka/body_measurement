# Body Measurements Tracker

A Django web application for tracking and managing body measurements over time. This application allows users to record, monitor, and visualize their body measurements, making it easier to track fitness progress or body changes.

## Features

- User authentication and personal accounts
- Record and track multiple body measurements
- English and Polish language support (i18n)
- Secure data storage
- Responsive UI (Bootstrap 5)

## Prerequisites

- Python 3.11+
- pip

## Local Setup

1. Clone the repository:
```bash
git clone <your-repository-url>
cd body_measurements
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file (see `.env.sample`) in the project root with:
```
DJANGO_SECRET_KEY=your_secret_key_here
DJANGO_DEBUG=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_email_app_password
```

5. Run database migrations:
```bash
python manage.py migrate
```

6. Create a superuser (admin account):
```bash
python manage.py createsuperuser
```

7. Start the development server:
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## Environment Variables

- `DJANGO_SECRET_KEY`: Django secret key
- `DJANGO_DEBUG`: 'True' for development, 'False' for production
- `DJANGO_ALLOWED_HOSTS`: Comma-separated list of hosts (default allows localhost and `.pythonanywhere.com`)
- `DJANGO_CSRF_TRUSTED_ORIGINS`: Comma-separated origins with scheme (default includes `https://*.pythonanywhere.com`)
- `EMAIL_HOST_USER` / `EMAIL_HOST_PASSWORD`: Optional for password reset emails. If unset in production, a dummy email backend is used to avoid runtime errors.

## Deployment (PythonAnywhere)

1) Create a virtualenv and install:
```bash
pip install -r requirements.txt
```

2) Set environment variables in the Web app (Environment section):
- `DJANGO_SECRET_KEY` (required)
- `DJANGO_DEBUG=False`
- `DJANGO_ALLOWED_HOSTS=yourusername.pythonanywhere.com`
- Optional: `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`

3) Configure WSGI to point to this project (module: `body_measurements.wsgi`).

4) Run migrations and create a superuser from a Bash console:
```bash
python manage.py migrate
python manage.py createsuperuser
```

5) Collect static files and map them:
```bash
python manage.py collectstatic --noinput
```
- In the Web tab, add a Static file mapping: URL `/static/` → path shown as `STATIC_ROOT` (see `body_measurements/settings.py`).

6) Reload the web app.

### Troubleshooting
- DisallowedHost or 400: set `DJANGO_ALLOWED_HOSTS` to your domain.
- CSRF verification failed: add `https://yourusername.pythonanywhere.com` to `DJANGO_CSRF_TRUSTED_ORIGINS`.
- ImportError: `python-dotenv`: ensure `pip install -r requirements.txt` ran (dotenv is required by settings).
- No such table / migrations: run `python manage.py migrate` in your virtualenv.
- Static files 404: run `collectstatic` and configure the static mapping in the Web tab.
- Email errors: either set `EMAIL_HOST_USER`/`EMAIL_HOST_PASSWORD` or rely on the default dummy backend in production.

## Contributing

Feel free to submit issues and enhancement requests.

## Security

For security issues, please email [your-email@example.com]

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
