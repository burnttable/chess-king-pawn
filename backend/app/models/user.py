from datetime import datetime
from ..db import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    token = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    games = db.relationship('Game', back_populates='user', cascade='all, delete-orphan')
    settings = db.relationship('UserSettings', back_populates='user', uselist=False, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'token': self.token,
            'created_at': self.created_at.isoformat()
        }
