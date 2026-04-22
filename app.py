import os

from flask import Flask, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash

from database.db import get_db, init_db, seed_db

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-change-me")

with app.app_context():
    init_db()
    seed_db()


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    if not email or not password:
        return render_template("login.html", error="Invalid email or password")

    conn = get_db()
    user = conn.execute(
        "SELECT id, name, password_hash FROM users WHERE email = ?", (email,)
    ).fetchone()
    conn.close()

    if user is None or not check_password_hash(user["password_hash"], password):
        return render_template("login.html", error="Invalid email or password")

    session.clear()
    session["user_id"] = user["id"]
    session["user_name"] = user["name"]
    return redirect(url_for("dashboard"))


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html", user_name=session["user_name"])


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("landing"))


@app.route("/profile")
def profile():
    if not session.get("user_id"):
        return redirect(url_for("login"))

    user = {
        "name": "Demo User",
        "email": "demo@spendly.com",
        "member_since": "22 Apr 2024",
    }
    stats = {
        "total_spent": "₹5,200",
        "transaction_count": 8,
        "top_category": "Bills",
    }
    transactions = [
        {"date": "18 Apr 2026", "description": "Grocery shopping",  "category": "Food",          "amount": "₹450"},
        {"date": "16 Apr 2026", "description": "Gift for friend",    "category": "Other",         "amount": "₹500"},
        {"date": "14 Apr 2026", "description": "New headphones",     "category": "Shopping",      "amount": "₹1,200"},
        {"date": "11 Apr 2026", "description": "Movie tickets",      "category": "Entertainment", "amount": "₹350"},
        {"date": "09 Apr 2026", "description": "Pharmacy",           "category": "Health",        "amount": "₹800"},
    ]
    categories = [
        {"name": "Bills",         "amount": "₹1,500", "percent": 29},
        {"name": "Shopping",      "amount": "₹1,200", "percent": 23},
        {"name": "Health",        "amount": "₹800",   "percent": 15},
        {"name": "Food",          "amount": "₹700",   "percent": 13},
        {"name": "Other",         "amount": "₹500",   "percent": 10},
        {"name": "Entertainment", "amount": "₹350",   "percent": 7},
        {"name": "Transport",     "amount": "₹150",   "percent": 3},
    ]
    return render_template("profile.html",
                           user=user, stats=stats,
                           transactions=transactions, categories=categories)


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    app.run(debug=True, port=5001)
