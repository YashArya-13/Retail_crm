import os

# Must be BEFORE importing Flask-Dance
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_dance.contrib.google import make_google_blueprint, google
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from config import Config
from models import db, User, Profile

# ---------------------------------------
# Load Environment Variables
# ---------------------------------------
load_dotenv()

# ---------------------------------------
# Flask App
# ---------------------------------------
app = Flask(__name__)
app.config.from_object(Config)

# Upload Folder
UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------------------------------------
# Database
# ---------------------------------------
db.init_app(app)

# ---------------------------------------
# Login Manager
# ---------------------------------------
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "Please login first."

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ---------------------------------------
# Google OAuth
# ---------------------------------------
google_bp = make_google_blueprint(
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    scope=[
        "openid",
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile",
    ]
)

app.register_blueprint(google_bp, url_prefix="/login")


# ---------------------------------------
# Home
# ---------------------------------------
@app.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


# ---------------------------------------
# Signup
# ---------------------------------------
@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        existing_user = User.query.filter(
            (User.username == username) |
            (User.email == email)
        ).first()

        if existing_user:
            flash("Username or Email already exists.", "danger")
            return redirect(url_for("signup"))

        hashed_password = generate_password_hash(password)

        new_user = User(
            username=username,
            email=email,
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        flash("Registration successful.", "success")

        return redirect(url_for("dashboard"))

    return render_template("signup.html")


# ---------------------------------------
# Login
# ---------------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and user.password and check_password_hash(user.password, password):

            login_user(user)
            flash("Login successful.", "success")

            return redirect(url_for("dashboard"))

        flash("Invalid username or password.", "danger")

    return render_template("login.html")


# ---------------------------------------
# Google Login
# ---------------------------------------
@app.route("/google-login")
def google_login():

    if not google.authorized:
        return redirect(url_for("google.login"))

    response = google.get("/oauth2/v2/userinfo")

    if not response.ok:
        flash("Google login failed.", "danger")
        return redirect(url_for("login"))

    info = response.json()

    email = info["email"]
    google_id = info["id"]
    username = email.split("@")[0]

    user = User.query.filter_by(email=email).first()

    if not user:

        user = User(
            username=username,
            email=email,
            google_id=google_id
        )

        db.session.add(user)
        db.session.commit()

    login_user(user)
    flash("Signed in with Google successfully.", "success")

    return redirect(url_for("dashboard"))


# ---------------------------------------
# Dashboard
# ---------------------------------------
@app.route("/dashboard")
@login_required
def dashboard():

    profile = Profile.query.filter_by(
        user_id=current_user.id
    ).first()

    return render_template(
        "dashboard.html",
        profile=profile
    )


# ---------------------------------------
# Profile
# ---------------------------------------
@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():

    profile = Profile.query.filter_by(
        user_id=current_user.id
    ).first()

    if request.method == "POST":

        full_name = request.form["full_name"]
        address = request.form["address"]
        education = request.form["education"]

        filename = None

        photo = request.files.get("photo")

        if photo and photo.filename != "":

            filename = secure_filename(photo.filename)

            photo.save(
                os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    filename
                )
            )

        if profile:

            profile.full_name = full_name
            profile.address = address
            profile.education = education

            if filename:
                profile.photo = filename

        else:

            profile = Profile(
                user_id=current_user.id,
                full_name=full_name,
                address=address,
                education=education,
                photo=filename
            )

            db.session.add(profile)

        db.session.commit()

        flash("Profile updated successfully.")

        return redirect(url_for("profile"))

    return render_template(
        "profile.html",
        profile=profile
    )


# ---------------------------------------
# Logout
# ---------------------------------------
@app.route("/logout")
@login_required
def logout():

    logout_user()

    flash("Logged out successfully.")

    return redirect(url_for("login"))


# ---------------------------------------
# Create Database
# ---------------------------------------
with app.app_context():
    db.create_all()


# ---------------------------------------
# Run App
# ---------------------------------------
if __name__ == "__main__":
    app.run(debug=True)