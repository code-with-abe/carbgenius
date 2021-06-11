from flask import Flask, render_template, request, redirect, url_for, g
import sqlite3

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/feedback", methods=["GET", "POST"])
def feedback():
    conn = get_db()
    c = conn.cursor()

    if request.method == "POST":
        # Process the form data
        c.execute("""INSERT INTO cg_feedback
                        (title, feedback)
                            VALUES (?,?)""",
                  (
                      request.form.get("title"),
                      request.form.get("feedback")
                  )
                  )
        conn.commit()
        # Redirect to some page
        return redirect(url_for("home"))

    return render_template("feedback.html")

@app.route("/upload", methods=["GET", "POST"])
def upload():
    conn = get_db()
    c = conn.cursor()

    if request.method == "POST":
        # Process the form data
        c.execute("""INSERT INTO cg_feedback
                        (title, feedback)
                            VALUES (?,?)""",
                  (
                      request.form.get("title"),
                      request.form.get("feedback")
                  )
                  )
        conn.commit()
        # Redirect to some page
        return redirect(url_for("home"))

    return render_template("upload.html")


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('db/carbgenius.db')
    return db
