# Spec: Login and Logout

## Overview

This step wires up the `POST /login` endpoint and the `GET /logout` endpoint, completing the authentication cycle started in Step 2 (registration). A visitor submits their email and password; the server looks up the user, verifies the hash, opens a Flask session, and redirects them to the dashboard. Logout clears that session and sends the user back to the landing page. After this step every protected route has a working gate.

## Depends on

- **Step 01 — Database Setup**: `users` table and `get_db()` must exist
- **Step 02 — Registration**: user records with hashed passwords must be insertable; `app.secret_key`, `session`, Flask imports, and `templates/dashboard.html` must already be in place

## Routes

- `POST /login` — validate credentials, set session, redirect to dashboard — public
- `GET /logout` — clear session, redirect to landing page — public (safe to hit even when logged out)

> `GET /login` already exists and renders `login.html`; it requires no changes.

## Database changes

No database changes. All required columns (`email`, `password_hash`) already exist in the `users` table from Step 01.

## Templates

- **Modify:** `templates/login.html` — already renders `{{ error }}`; no structural changes needed
- **No new templates required**

## Files to change

- `app.py` — implement `POST /login` logic and replace the `GET /logout` stub

## Files to create

None

## New dependencies

No new dependencies. Uses:
- `sqlite3` (standard library)
- `werkzeug.security.check_password_hash` (already installed)
- `flask.session`, `flask.redirect`, `flask.url_for`, `flask.request` (already imported in Step 02)

## Rules for implementation

- No SQLAlchemy or ORMs — raw `sqlite3` only
- Parameterised queries only — never string-format SQL
- Passwords verified with `werkzeug.security.check_password_hash`
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- On login failure, re-render `login.html` with a generic error message (do **not** reveal whether the email exists or the password is wrong — both cases return "Invalid email or password")
- Session stores `user_id` (int) and `user_name` (str) — same keys used by the dashboard in Step 02
- `logout` must call `session.clear()`, then `redirect(url_for('landing'))`
- The `POST /login` route must be added as a **separate decorator** on the existing `/login` view or as a new function — do not merge GET and POST into one function unless using `methods=["GET", "POST"]` cleanly
- After successful login, redirect to `url_for('dashboard')`

## Definition of done

- [ ] Submitting the login form with correct credentials redirects to `/dashboard` and shows the user's name
- [ ] Submitting with a wrong password re-renders `login.html` with "Invalid email or password"
- [ ] Submitting with an unknown email re-renders `login.html` with "Invalid email or password" (same message — no email-enumeration leak)
- [ ] Submitting with empty fields re-renders `login.html` with "Invalid email or password"
- [ ] Visiting `/logout` clears the session and redirects to `/` (landing page)
- [ ] After logout, visiting `/dashboard` redirects back to `/login`
- [ ] The demo seed user (`demo@spendly.com` / `demo123`) can log in successfully
- [ ] Navbar shows Dashboard / Sign-out when logged in, Sign-in / Get-started when logged out
