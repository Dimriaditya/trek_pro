from flask import Flask, render_template, request, Response, send_from_directory
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

@app.route("/kedarkantha")
def kedarkantha():
    return render_template("kedarkantha.html")

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


# ---------------- ADMIN ---------------
@app.route("/admin")
def admin():

    auth = request.authorization

    if not auth or auth.username != "akash semwal" or auth.password != "dimri@#&$4927":
        return Response(
            "Login Required",
            401,
            {"WWW-Authenticate": 'Basic realm="Login Required"'}
        )

    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("SELECT * FROM bookings ORDER BY id DESC")
    data = cur.fetchall()
    conn.close()

    return render_template("admin.html", data=data)
@app.route("/robots.txt")
def robots():
    return send_from_directory("static", "robots.txt")

@app.route("/sitemap.xml")
def sitemap():
    return send_from_directory("static", "sitemap.xml")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

