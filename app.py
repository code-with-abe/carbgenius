from flask import Flask, render_template, request, redirect, url_for, g, flash
import sqlite3
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import StringField, TextAreaField, SubmitField, FileField, SelectField, DecimalField
from wtforms.validators import InputRequired, DataRequired, Length
from werkzeug.utils import secure_filename
import os
import datetime
from secrets import token_hex

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config["SECRET_KEY"] = "secretkey"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["jpeg", "jpg", "png"]
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024
app.config["IMAGE_UPLOADS"] = os.path.join(basedir, "uploads")


class NewFeedbackForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired("Input is required!"), DataRequired("Data is required!"),
                                             Length(min=5, max=20,
                                                    message="Input must be between 5 and 20 characters long")])
    feedback = TextAreaField("Feedback",
                             validators=[InputRequired("Input is required!"), DataRequired("Data is required!"),
                                         Length(min=5, max=20,
                                                message="Input must be between 5 and 20 characters long")])
    submit = SubmitField("Submit")


class NewPictureForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired("Input is required!"), DataRequired("Data is required!"),
                                             Length(min=5, max=20,
                                                    message="Input must be between 5 and 20 characters long")])
    feedback = TextAreaField("Feedback",
                             validators=[InputRequired("Input is required!"), DataRequired("Data is required!"),
                                         Length(min=5, max=20,
                                                message="Input must be between 5 and 20 characters long")])

    image = FileField("Image",
                      validators=[FileRequired(), FileAllowed(app.config["ALLOWED_IMAGE_EXTENSIONS"], "Images only!")])
    restaurant = SelectField("Restaurant", coerce=int)
    submit = SubmitField("Submit")


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/feedback", methods=["GET", "POST"])
def feedback():
    conn = get_db()
    c = conn.cursor()
    form = NewFeedbackForm()

    if request.method == "POST":
        # Process the form data
        c.execute("""INSERT INTO cg_feedback
                        (title, feedback)
                            VALUES (?,?)""",
                  (
                      form.title.data,
                      form.feedback.data
                  )
                  )
        conn.commit()
        # Redirect to some page
        flash("Your Feedback {} has been successfully submitted".format(request.form.get("title")), "success")
        return redirect(url_for("home"))

    return render_template("feedback.html", form=form)


@app.route("/upload", methods=["GET", "POST"])
def upload():
    conn = get_db()
    c = conn.cursor()
    form = NewPictureForm()

    c.execute("SELECT id,restaurant_name FROM cg_restaurants")
    restaurants = c.fetchall()
    form.restaurant.choices = restaurants

    if form.validate_on_submit():
        format = "%Y%m%dT%H%M%S"
        now = datetime.datetime.utcnow().strftime(format)
        random_string = token_hex(2)
        filename = random_string + "_" + now + "_" + form.image.data.filename
        filename = secure_filename(filename)
        form.image.data.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
        # Process the form data
        c.execute("""INSERT INTO cg_feedback
                        (title, feedback)
                            VALUES (?,?)""",
                  (
                      form.title.data,
                      form.feedback.data
                  )
                  )
        conn.commit()
        # Redirect to some page
        flash("Item {} has been successfully submitted".format(request.form.get("title")), "success")
        return redirect(url_for("home"))

    if form.errors:
        flash("{}".format(form.errors), "danger")
    return render_template("upload.html", form=form)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('db/carbgenius.db')
    return db
