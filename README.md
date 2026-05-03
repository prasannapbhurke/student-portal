# Student Portal

Student Portal is a Django-based study management application for students who want one place for notes, homework, tasks, study logs, and quick reference tools.

The project combines classic CRUD workflows with small study utilities such as dictionary lookup, Wikipedia search, YouTube search, a calendar view, conversion references, a timer, flashcards, and quizzes.

## Overview

The application is built around one Django app named `dashboard`. It provides:

- account signup and login
- note creation, editing, filtering, bulk deletion, and CSV export
- homework tracking with deadlines and status
- todo management with subtasks, priorities, categories, due dates, and progress
- study session logging and summary metrics
- quick-access tools for books, dictionary, conversions, Wikipedia, and YouTube
- an enhanced homepage with summary cards, theme switching, and tool shortcuts

Main project path:

`project file/Youtube/django/studentstudyportal`

## Tech Stack

- Python
- Django 6
- Bootstrap 4
- WhiteNoise for static file serving
- Gunicorn for production
- `dj-database-url` for database configuration
- optional Celery + Redis for background export jobs
- optional `requests` for external API calls

## Repository Layout

Top-level files:

- `README.md` - project documentation
- `CHANGELOG.md` - change history
- `requirements.txt` - Python dependencies
- `Procfile` - production start command
- `install.bat` - Windows setup helper

Main Django project:

- `project file/Youtube/django/studentstudyportal/manage.py`
- `project file/Youtube/django/studentstudyportal/studentstudyportal/` - settings, URLs, WSGI
- `project file/Youtube/django/studentstudyportal/dashboard/` - app models, views, forms, templates, tasks, tests
- `project file/Youtube/django/studentstudyportal/static/` - shared CSS and static assets

## Core Features

### 1. Authentication

- user signup
- Django auth login/logout
- protected pages for notes, homework, todos, calendar, study sessions, and exports

### 2. Homepage

The homepage acts as the main landing dashboard and shows:

- quick actions
- summary counts for notes, homework, todos, books, dictionary entries, conversions, and study sessions
- shortcuts to all major study tools
- theme controls with saved browser preference

### 3. Notes

Notes support:

- add/edit/delete
- title and description fields
- keyword filtering
- date range filtering
- bulk delete
- CSV export

Exports are attempted through Celery first and fall back to synchronous generation if Celery is unavailable.

### 4. Homework

Homework records include:

- title
- description
- subject
- deadline
- status (`pending`, `completed`, `submitted`)

Homework pages support:

- add/edit/delete
- filtering by keyword
- filtering by status
- ordered display by deadline

### 5. Todo Management

Todos include:

- title
- description
- priority
- category
- progress
- completion flag
- due date

Todo pages support:

- add/edit
- mark complete
- subtask creation
- subtask toggling
- automatic progress update based on completed subtasks
- overdue count display

### 6. Study Sessions

Study sessions help track focused study time with:

- subject
- duration in minutes
- date
- notes

The app also calculates total recorded study time for dashboard summaries.

### 7. Study Utilities

The portal includes several utility pages:

- `Books` - static/reference list from database
- `Dictionary` - local dictionary lookup, fuzzy local match, online fallback, external dictionary redirect fallback
- `Wikipedia` - redirects to best matching article when possible
- `YouTube` - redirects directly to YouTube if embedded API search is unavailable
- `Conversion` - database-backed conversion reference table
- `Calendar` - combines homework and todo deadlines into one date-based view
- `Timer` - study timer page
- `Flashcards` - lightweight in-browser revision deck builder
- `Quizzes` - lightweight in-browser practice quiz builder

## Search and External Lookup Behavior

### YouTube

- If `YOUTUBE_API_KEY` is configured and API access works, the app can show embedded video search results.
- If the key is missing or the request fails, the app redirects directly to YouTube search results.

### Wikipedia

- The app tries Wikipedia's search API first.
- If a close article is found, the user is redirected directly to that article.
- If that lookup fails, the app redirects to Wikipedia search results.

### Dictionary

- The app first looks for an exact local dictionary match.
- If that fails, it tries a close local match using fuzzy matching.
- If that also fails, it queries an online dictionary API.
- If no definition is found, it redirects to Dictionary.com for the searched word.

## Data Model

Main models in `dashboard/models.py`:

- `Note`
- `Homework`
- `Todo`
- `Subtask`
- `Book`
- `DictionaryEntry`
- `ConversionEntry`
- `StudySession`
- `Export`

### Model Notes

- Most study-owned records are linked to Django `User`.
- `Export` stores CSV export data and status.
- `Todo` progress can be updated manually or derived from subtasks.
- `Homework` and `Todo` power the calendar page.

## Forms

Forms are defined in `dashboard/forms.py`:

- `NoteForm`
- `HomeworkForm`
- `TodoForm`
- `SubtaskForm`
- `StudySessionForm`

These forms use Bootstrap-friendly widgets for the current UI.

## URL Map

Main routes in `dashboard/urls.py`:

- `/` - homepage
- `/dashboard/` - progress dashboard
- `/signup/`
- `/notes/`
- `/add-note/`
- `/edit-note/<id>/`
- `/delete-note/<id>/`
- `/export-notes/`
- `/exports/`
- `/download-export/<id>/`
- `/homework/`
- `/add-homework/`
- `/edit-homework/<id>/`
- `/delete-homework/<id>/`
- `/todo/`
- `/add-todo/`
- `/edit-todo/<id>/`
- `/mark-todo-complete/<id>/`
- `/add-subtask/<todo_id>/`
- `/toggle-subtask/<id>/`
- `/books/`
- `/dictionary/`
- `/conversion/`
- `/youtube/`
- `/wiki/`
- `/calendar/`
- `/study-sessions/`
- `/add-study-session/`
- `/timer/`
- `/flashcards/`
- `/quizzes/`

Authentication routes are provided through:

- `/accounts/login/`
- `/accounts/logout/`

## Local Setup

### Option A: Manual setup

1. Create a virtual environment:

```powershell
python -m venv venv
```

2. Activate it:

```powershell
venv\Scripts\activate
```

3. Install dependencies:

```powershell
pip install -r requirements.txt
```

4. Move into the Django project:

```powershell
cd "project file\Youtube\django\studentstudyportal"
```

5. Apply migrations:

```powershell
python manage.py migrate
```

6. Run the server:

```powershell
python manage.py runserver
```

7. Open the app:

[http://127.0.0.1:8000](http://127.0.0.1:8000)

### Option B: Windows helper

You can also use:

```powershell
install.bat
```

This script:

- checks Python
- creates a virtual environment if needed
- installs requirements
- runs migrations
- collects static files

## Environment Variables

The project reads the following environment variables when available:

- `SECRET_KEY`
- `DEBUG`
- `ALLOWED_HOSTS`
- `SECURE_SSL_REDIRECT`
- `CELERY_BROKER_URL`
- `YOUTUBE_API_KEY`

### Example `.env` values

```env
SECRET_KEY=change-me
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
SECURE_SSL_REDIRECT=False
CELERY_BROKER_URL=redis://localhost:6379/0
YOUTUBE_API_KEY=
```

## Static Files and Themes

- Shared UI styles live in `static/css/main.css`.
- The navbar includes:
  - dark mode toggle
  - color theme chips
- Theme preference is stored in browser `localStorage`.
- In local development, static files are served directly from the current source tree.

## Exports and Background Jobs

`dashboard/tasks.py` contains the notes export task.

Behavior:

- If Celery is installed and working, note export can run as a background task.
- If Celery or Redis is unavailable, the project falls back to direct execution so exports still work locally.

## Testing

Run tests from the Django project directory:

```powershell
cd "project file\Youtube\django\studentstudyportal"
python manage.py test dashboard
python manage.py check
```

Current test coverage focuses on:

- YouTube fallback redirect behavior
- Wikipedia best-match and search fallback behavior
- dictionary lookup behavior
- logout redirect behavior

## Deployment

The repository includes a `Procfile` for production startup:

```text
web: cd "project file/Youtube/django/studentstudyportal" && gunicorn studentstudyportal.wsgi:application --bind 0.0.0.0:$PORT
```

### Deployment Notes

- Set `SECRET_KEY` in production.
- Set `DEBUG=False` in production.
- Configure `ALLOWED_HOSTS`.
- Use a production database through `DATABASE_URL` if needed.
- Run `collectstatic` during deployment.
- Configure Redis only if you want true Celery background execution.

## Current Limitations

- Flashcards and quizzes are currently lightweight client-side tools, not database-backed study systems.
- Timer is a simple page and not yet connected to study session persistence.
- There is no full subject/course management model yet.
- There is no global cross-feature search yet.

## Suggested Next Improvements

- add `.gitignore` to exclude `db.sqlite3`, `__pycache__`, and local artifacts
- add `.env.example`
- make flashcards and quizzes database-backed
- connect timer output to study session logging
- add subject-based organization across notes, homework, and todos
- expand automated test coverage for CRUD flows and auth

## Changelog

Recent changes are documented in:

[CHANGELOG.md](/C:/Users/PRASANNA/Desktop/student portal/CHANGELOG.md)
