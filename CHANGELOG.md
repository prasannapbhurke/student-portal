# Changelog

All notable changes to this project will be documented in this file.

## 2026-05-03

- Fixed the YouTube search experience so it still works without a configured `YOUTUBE_API_KEY` by offering a direct YouTube search link.
- Fixed the Wikipedia search experience so users can still open the relevant Wikipedia page even when the API summary is unavailable.
- Fixed broken Wikipedia result styling caused by overly aggressive global card paragraph CSS.
- Added focused tests for YouTube and Wikipedia fallback behavior.
- Made `celery`, `crispy_forms`, and `requests` optional at runtime so the project can start more reliably in lightweight local environments.
- Added a fallback `crispy` template filter for environments where `django-crispy-forms` is not installed.
- Added a root `README.md` with setup, run, test, and deployment instructions.
