# Student Portal

A Django-based student study portal for managing notes, homework, todos, study sessions, and quick learning utilities such as Wikipedia search, YouTube search, dictionary lookup, books, calendar views, and unit conversion.

## Project Layout

The main Django project lives here:

`project file/Youtube/django/studentstudyportal`

Useful top-level files:

- `requirements.txt` - Python dependencies
- `Procfile` - production start command
- `install.bat` - local setup helper

## Features

- User signup and login
- Notes with search, filters, bulk delete, and CSV export
- Homework tracking with deadlines and status
- Todo management with subtasks and progress tracking
- Study sessions and dashboard stats
- Calendar view for upcoming work
- Books, dictionary, and conversion utilities
- Wikipedia search with direct open fallback
- YouTube search with direct open fallback when API configuration is missing
- Timer, flashcards, and quizzes pages

## Local Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Go to the Django project directory:

```powershell
cd "project file\Youtube\django\studentstudyportal"
```

4. Run migrations if needed:

```powershell
python manage.py migrate
```

5. Start the development server:

```powershell
python manage.py runserver
```

6. Open the app:

`http://127.0.0.1:8000/`

## Environment Variables

These settings are read from the environment when provided:

- `SECRET_KEY`
- `DEBUG`
- `ALLOWED_HOSTS`
- `SECURE_SSL_REDIRECT`
- `CELERY_BROKER_URL`
- `YOUTUBE_API_KEY`

## YouTube and Wikipedia Behavior

- If `YOUTUBE_API_KEY` is configured, the YouTube page can load embedded search results.
- If the API key is missing, the page still provides a direct YouTube search link.
- Wikipedia search shows summaries when available and still provides a direct Wikipedia link when the API cannot return a summary.

## Running Tests

From the Django project directory:

```powershell
python manage.py test dashboard
python manage.py check
```

## Deployment

The included `Procfile` starts the Django app with Gunicorn:

```text
web: cd "project file/Youtube/django/studentstudyportal" && gunicorn studentstudyportal.wsgi:application --bind 0.0.0.0:$PORT
```
