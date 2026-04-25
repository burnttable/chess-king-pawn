from datetime import datetime
from ..db import db

class Game(db.Model):
    __tablename__ = 'games'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    fen = db.Column(db.String(100), nullable=False)
    difficulty = db.Column(db.String(10), nullable=False)
    timer_enabled = db.Column(db.Boolean, default=False)
    timer_duration = db.Column(db.Integer)
    timer_remaining = db.Column(db.Integer)
    status = db.Column(db.String(20), default='in_progress')
    result = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user = db.relationship('User', back_populates='games')
    moves = db.relationship('Move', back_populates='game', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'fen': self.fen,
            'difficulty': self.difficulty,
            'timer_enabled': self.timer_enabled,
            'timer_duration': self.timer_duration,
            'timer_remaining': self.timer_remaining,
            'status': self.status,
            'result': self.result,
            'created_at': self.created_at.isoformat()
        }
