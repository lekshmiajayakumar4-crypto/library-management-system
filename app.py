from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

# ---------------- DATABASE ----------------
def init_db():
    conn = sqlite3.connect("library.db")
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            author TEXT,
            status TEXT,
            member_name TEXT,
            contact TEXT,
            issue_date TEXT,
            return_date TEXT
        )
    """)

    conn.commit()
    conn.close()

init_db()


# ---------------- HOME + SEARCH ----------------
@app.route("/", methods=["GET", "POST"])
def index():
    conn = sqlite3.connect("library.db")
    cur = conn.cursor()

    if request.method == "POST":
        search = request.form.get("search")
        cur.execute("""
            SELECT * FROM books
            WHERE name LIKE ? OR author LIKE ?
        """, ('%' + search + '%', '%' + search + '%'))
    else:
        cur.execute("SELECT * FROM books")

    books = cur.fetchall()
    conn.close()

    return render_template("index.html", books=books)


# ---------------- ADD BOOK ----------------
@app.route("/add", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        name = request.form["name"]
        author = request.form["author"]

        conn = sqlite3.connect("library.db")
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO books 
            (name, author, status, member_name, contact, issue_date, return_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (name, author, "Available", "", "", "", ""))

        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("add.html")


# ---------------- ISSUE BOOK ----------------
@app.route("/issue/<int:id>", methods=["GET", "POST"])
def issue_book(id):
    if request.method == "POST":
        member = request.form["member"]
        contact = request.form["contact"]
        issue_date = datetime.now().strftime("%Y-%m-%d")

        conn = sqlite3.connect("library.db")
        cur = conn.cursor()

        cur.execute("""
            UPDATE books
            SET status=?, member_name=?, contact=?, issue_date=?, return_date=?
            WHERE id=?
        """, ("Issued", member, contact, issue_date, "", id))

        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("issue.html")


# ---------------- RETURN BOOK ----------------
@app.route("/return/<int:id>")
def return_book(id):
    return_date = datetime.now().strftime("%Y-%m-%d")

    conn = sqlite3.connect("library.db")
    cur = conn.cursor()

    cur.execute("""
        UPDATE books
        SET status=?, member_name=?, contact=?, issue_date=?, return_date=?
        WHERE id=?
    """, ("Available", "", "", "", return_date, id))

    conn.commit()
    conn.close()

    return redirect("/")


# ---------------- DELETE BOOK ----------------
@app.route("/delete/<int:id>")
def delete_book(id):
    conn = sqlite3.connect("library.db")
    cur = conn.cursor()

    cur.execute("DELETE FROM books WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)