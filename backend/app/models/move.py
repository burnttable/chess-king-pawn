from ..db import db

class Move(db.Model):
    __tablename__ = 'moves'

    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)
    move_number = db.Column(db.Integer, nullable=False)
    from_square = db.Column(db.String(2), nullable=False)
    to_square = db.Column(db.String(2), nullable=False)
    piece = db.Column(db.String(10), nullable=False)
    fen_after = db.Column(db.String(100), nullable=False)

    # Relationships
    game = db.relationship('Game', back_populates='moves')

    def to_dict(self):
        return {
            'id': self.id,
            'game_id': self.game_id,
            'move_number': self.move_number,
            'from_square': self.from_square,
            'to_square': self.to_square,
            'piece': self.piece,
            'fen_after': self.fen_after
        }
