from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

DB = "bookings.db"

# ---------------- HOME ----------------
@app.route("/")
def home():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM bookings")
    total = cur.fetchone()[0]
    conn.close()

    return render_template("index.html", total=total)


# ---------------- BOOKING ----------------
@app.route("/book", methods=["POST"])
def book():
    data = (
        request.form["name"],
        request.form["email"],
        request.form["phone"],
        request.form["trek"],
        request.form["people"],
        request.form["days"],
        request.form["message"]
    )

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO bookings
        (name,email,phone,trek,people,days,message)
        VALUES (?,?,?,?,?,?,?)
    """, data)

    conn.commit()
    conn.close()

    return render_template("success.html", name=data[0], trek=data[3])


# ---------------- ADMIN ----------------
@app.route("/admin")
def admin():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("SELECT * FROM bookings ORDER BY id DESC")
    data = cur.fetchall()
    conn.close()

    return render_template("admin.html", data=data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

