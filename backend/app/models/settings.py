from ..db import db

class UserSettings(db.Model):
    __tablename__ = 'user_settings'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    theme = db.Column(db.String(10), default='light')
    default_difficulty = db.Column(db.String(10), default='medium')
    timer_enabled = db.Column(db.Boolean, default=False)
    default_timer_duration = db.Column(db.Integer, default=600)

    # Relationships
    user = db.relationship('User', back_populates='settings')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'theme': self.theme,
            'default_difficulty': self.default_difficulty,
            'timer_enabled': self.timer_enabled,
            'default_timer_duration': self.default_timer_duration
        }
