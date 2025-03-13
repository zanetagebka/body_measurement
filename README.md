# Body Measurements Tracker

A Django web application for tracking and managing body measurements over time. This application allows users to record, monitor, and visualize their body measurements, making it easier to track fitness progress or body changes.

## Features

- User authentication and personal accounts
- Record and track multiple body measurements
- Support for English and Polish languages
- Secure data storage
- Responsive design for both desktop and mobile use

## Prerequisites

- Python 3.x
- pip (Python package installer)

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

3. Install required dependencies:
```bash
pip install django django-widget-tweaks python-dotenv
```

4. Create a `.env` file in the project root with the following variables:
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

- `DJANGO_SECRET_KEY`: Django secret key for security
- `DJANGO_DEBUG`: Set to 'True' for development, 'False' for production
- `EMAIL_HOST_USER`: Gmail address for sending emails
- `EMAIL_HOST_PASSWORD`: Gmail app password for email functionality

## Deployment

The application is configured to be deployable on PythonAnywhere or similar hosting services. Make sure to:

1. Set `DEBUG=False` in production
2. Configure your production database
3. Set up proper email settings
4. Configure static files

## Contributing

Feel free to submit issues and enhancement requests.

## Security

For security issues, please email [your-email@example.com]

## License

This project is licensed under the MIT License - see the LICENSE file for details. 