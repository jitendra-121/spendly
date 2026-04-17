import os
import sqlite3
from datetime import date

from werkzeug.security import generate_password_hash

# Resolve project root (one level up from this file's directory)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "spendly.db")


def get_db() -> sqlite3.Connection:
    """Open a SQLite connection with Row factory and foreign keys enabled."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    """Create all tables if they don't already exist."""
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now'))
        );

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
    """)
    conn.commit()
    conn.close()


def seed_db() -> None:
    """Insert demo user and sample expenses. Skips if data already exists."""
    conn = get_db()

    # Guard: don't seed if users already exist
    count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    if count > 0:
        conn.close()
        return

    # Insert demo user with hashed password
    password_hash = generate_password_hash("demo123")
    conn.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        ("Demo User", "demo@spendly.com", password_hash),
    )

    # Build 8 sample expenses spread across the current month
    today = date.today()
    expenses = [
        (1, 250.00, "Food", date(today.year, today.month, 2).isoformat(), "Lunch at cafe"),
        (1, 150.00, "Transport", date(today.year, today.month, 4).isoformat(), "Auto rickshaw"),
        (1, 1500.00, "Bills", date(today.year, today.month, 6).isoformat(), "Electricity bill"),
        (1, 800.00, "Health", date(today.year, today.month, 9).isoformat(), "Pharmacy"),
        (1, 350.00, "Entertainment", date(today.year, today.month, 11).isoformat(), "Movie tickets"),
        (1, 1200.00, "Shopping", date(today.year, today.month, 14).isoformat(), "New headphones"),
        (1, 500.00, "Other", date(today.year, today.month, 16).isoformat(), "Gift for friend"),
        (1, 450.00, "Food", date(today.year, today.month, 18).isoformat(), "Grocery shopping"),
    ]

    conn.executemany(
        "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
        expenses,
    )

    conn.commit()
    conn.close()