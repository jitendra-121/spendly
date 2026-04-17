# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run the development server (port 5001)
python app.py

# Or with Flask CLI
flask --app app run --debug --port 5001

# Run tests
pytest

# Run tests with coverage
pytest --cov=. --cov-report=term-missing

# Run a single test file
pytest tests/test_auth.py

# Install dependencies
pip install -r requirements.txt
```

## Architecture

**Spendly** is a Flask expense-tracker app using SQLite and Jinja2 templates. It is structured as a **step-by-step tutorial skeleton** — several routes in `app.py` are intentional stubs that learners implement progressively.

### Request flow

```
Browser → app.py route → Jinja2 template (extends base.html) → rendered HTML
                        ↓
                   database/db.py  ←  SQLite (expenses.db)
```

### Key files

| File | Role |
|---|---|
| `app.py` | All Flask routes — implemented and stub alike |
| `database/db.py` | **Learner-implemented** — `get_db()`, `init_db()`, `seed_db()` |
| `templates/base.html` | Layout shell: navbar, footer, loads `style.css` + `main.js` |
| `static/css/style.css` | Global design system (DM Sans / DM Serif Display, teal palette) |
| `static/css/landing.css` | Landing-page-only styles, loaded via `{% block head %}` |
| `static/js/main.js` | Stub — learner adds JS here as features are built |

### Template inheritance

All pages `{% extends "base.html" %}`. The base provides the navbar (Sign in / Get started) and footer (Terms, Privacy links). The landing page is the only template that also loads `landing.css` via `{% block head %}`, and embeds its own inline `<script>` for the YouTube demo modal via `{% block scripts %}`.

### Database layer (not yet implemented)

`database/db.py` is intentionally empty. When implemented it should expose:
- `get_db()` — SQLite connection with `row_factory = sqlite3.Row` and `PRAGMA foreign_keys = ON`
- `init_db()` — `CREATE TABLE IF NOT EXISTS` for all tables
- `seed_db()` — sample data for development

### Stub routes (learner implements these)

- `GET /logout` — Step 3
- `GET /profile` — Step 4
- `GET /expenses/add` — Step 7
- `GET /expenses/<id>/edit` — Step 8
- `GET /expenses/<id>/delete` — Step 9

### Video modal

The landing page `#see-how-btn` opens a YouTube embed modal. The YouTube video ID is a placeholder (`VIDEO_ID`) in `landing.html:129` — replace it with the real ID when the demo video is ready.

### Design tokens

- **Fonts**: DM Serif Display (headings), DM Sans 300–600 (body)
- **Currency**: Indian Rupee (₹)
- **Brand icon**: `◈`