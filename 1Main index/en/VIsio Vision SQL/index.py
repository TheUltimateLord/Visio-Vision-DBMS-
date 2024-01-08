from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

# Additional model classes can be added for more features

@app.route("/")
def index():
    users = User.query.all()
    return render_template("index.html", users=users)

@app.route("/add_user", methods=["GET", "POST"])
def add_user():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")

        new_user = User(username=username, email=email)
        db.session.add(new_user)
        db.session.commit()

        flash("User added successfully", "success")
        return redirect(url_for("index"))

    return render_template("add_user.html")

if __name__ == "__main__":
    app.secret_key = 'supersecretkey'  # Used for flashing messages
    db.create_all()
    app.run(debug=True)
