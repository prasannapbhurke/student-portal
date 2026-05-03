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
- Updated the YouTube workflow to redirect directly to YouTube results instead of showing an in-app fallback message.
- Updated the Wikipedia workflow to redirect to the best matching article when possible, with a search-result fallback for misspelled queries.
- Fixed the navbar theme script and made saved theme preferences work more reliably.
- Refreshed the homepage with a stronger hero section, quick actions, highlight cards, and improved feature-card spacing.
- Expanded the documentation to cover themes, search behavior, and the enhanced homepage.
- Replaced the short README with full project documentation covering architecture, features, models, routes, setup, testing, deployment, and current limitations.
