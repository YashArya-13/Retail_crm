from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100), unique=True, nullable=False)

    email = db.Column(db.String(150), unique=True, nullable=False)

    password = db.Column(db.String(255), nullable=True)

    google_id = db.Column(db.String(255), nullable=True)

    profile = db.relationship(
        "Profile",
        backref="user",
        uselist=False,
        cascade="all, delete"
    )


class Profile(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    photo = db.Column(db.String(255))

    full_name = db.Column(db.String(150))

    address = db.Column(db.Text)

    education = db.Column(db.Text)