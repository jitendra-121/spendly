# Plan: Database Setup (Step 1)

## Context

Spendly has no data layer yet. `database/db.py` is a stub with comments only. All future features (auth, profile, expenses) depend on this foundation being correctly implemented. No new routes or templates — this is purely backend plumbing.

**Spec**: `.claude/specs/01-database-setup.md`
**Branch**: `feature/database-setup`

---

## Files to Modify

| File | What changes |
|------|-------------|
| `database/db.py` | Replace stub with `get_db()`, `init_db()`, `seed_db()` |
| `app.py` | Import db functions, call `init_db()` + `seed_db()` on startup |

No new files to create.

---

## Implementation Steps

### Step 1: `get_db()` in `database/db.py`

- Open SQLite connection to `spendly.db` in **project root** (use `os.path` to resolve path relative to `db.py`'s parent directory)
- Set `connection.row_factory = sqlite3.Row` for dict-like row access
- Execute `PRAGMA foreign_keys = ON` on every connection
- Return the connection

### Step 2: `init_db()` in `database/db.py`

- Call `get_db()` to get a connection
- Execute `CREATE TABLE IF NOT EXISTS` for both tables:

**users table:**
```sql
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TEXT DEFAULT (datetime('now'))
);
```

**expenses table:**
```sql
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    date TEXT NOT NULL,
    description TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

- Commit and close the connection

### Step 3: `seed_db()` in `database/db.py`

- Call `get_db()` to get a connection
- **Guard**: Check if `users` table already has rows → return early if yes (prevents duplicate seed data)
- Insert 1 demo user:
  - name: `Demo User`
  - email: `demo@spendly.com`
  - password: `demo123` hashed via `werkzeug.security.generate_password_hash`
- Insert 8 sample expenses linked to the demo user (user_id = 1):
  - Cover all 7 categories: Food, Transport, Bills, Health, Entertainment, Shopping, Other (one category gets 2 expenses)
  - Dates spread across the current month (use `datetime.date.today()` to compute)
  - Realistic amounts in ₹ (e.g., 250.00 for Food, 1500.00 for Bills)
- Commit and close the connection

**Categories (fixed list):** Food, Transport, Bills, Health, Entertainment, Shopping, Other

### Step 4: Wire up `app.py`

- Add import: `from database.db import get_db, init_db, seed_db`
- After `app = Flask(__name__)`, add:
  ```python
  with app.app_context():
      init_db()
      seed_db()
  ```
- No changes to existing routes

---

## Constraints

- **No ORMs** — raw `sqlite3` only
- **Parameterized queries only** — never use f-strings or `.format()` in SQL
- `PRAGMA foreign_keys = ON` on every connection
- Passwords hashed with `werkzeug.security.generate_password_hash`
- Dates in `YYYY-MM-DD` format
- `seed_db()` must be idempotent (safe to call multiple times)

---

## Dependencies

- `sqlite3` — stdlib, no install needed
- `werkzeug.security` — already installed (comes with Flask)

---

## Verification

1. **Start the app**: `python app.py` — should start without errors
2. **Check DB file**: `spendly.db` should appear in project root
3. **Verify tables**:
   ```bash
   sqlite3 spendly.db ".tables"
   # → expenses  users
   ```
4. **Verify schema**:
   ```bash
   sqlite3 spendly.db ".schema users"
   sqlite3 spendly.db ".schema expenses"
   ```
5. **Verify seed data**:
   ```bash
   sqlite3 spendly.db "SELECT id, name, email FROM users;"
   # → 1|Demo User|demo@spendly.com
   sqlite3 spendly.db "SELECT COUNT(*) FROM expenses;"
   # → 8
   sqlite3 spendly.db "SELECT DISTINCT category FROM expenses;"
   # → all 7 categories
   ```
6. **Verify idempotency**: Restart app, check `SELECT COUNT(*) FROM users;` still returns 1
7. **Verify foreign keys**:
   ```bash
   sqlite3 spendly.db "PRAGMA foreign_keys = ON; INSERT INTO expenses (user_id, amount, category, date) VALUES (999, 100, 'Food', '2026-01-01');"
   # → should fail with FOREIGN KEY constraint error
   ```

---

## Definition of Done

- [ ] `spendly.db` created on app startup
- [ ] Both tables exist with correct schema and constraints
- [ ] Demo user exists with hashed password
- [ ] 8 sample expenses across all 7 categories
- [ ] No duplicate seed data on repeated runs
- [ ] App starts without errors
- [ ] Foreign key enforcement works
- [ ] All queries use parameterized SQL
