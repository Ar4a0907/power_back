from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from .config import ADMIN_ROLE, ADMIN_STATUS


db = SQLAlchemy()
dbSession = db.session


class Admin(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)

    # Admin Authentication fields
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    loginAttempts = db.Column(db.SmallInteger, default=0)

    # Admin fields
    name = db.Column(db.String(50), nullable=True)
    surname = db.Column(db.String(50), nullable=True)

    status = db.Column(db.SmallInteger, default=ADMIN_STATUS['created'])
    role = db.Column(db.SmallInteger, default=ADMIN_ROLE['admin'])
    created = db.Column(db.DateTime, default=datetime.utcnow)
