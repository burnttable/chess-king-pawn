from flask import Blueprint, request, jsonify
from ..db import db
from ..models.user import User
from ..models.game import Game
from ..models.move import Move
from ..models.settings import UserSettings
from ..services.auth_service import verify_token
from ..services.chess_logic import ChessBoard

game_bp = Blueprint('game', __name__)

def get_user_from_token():
    """Get user from Authorization header token"""
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return None
    token = auth_header.split(' ')[1]
    return verify_token(token)

@game_bp.route('/start', methods=['POST'])
def start_game():
    """Start a new game"""
    user = get_user_from_token()
    if not user:
        return jsonify({'error': 'Invalid or missing token'}), 401

    data = request.get_json()

    # Get difficulty (default to user's default or 'medium')
    difficulty = data.get('difficulty', 'medium')
    if difficulty not in ['easy', 'medium', 'hard']:
        return jsonify({'error': 'Invalid difficulty'}), 400

    # Get timer settings
    timer_enabled = data.get('timer_enabled', False)
    timer_duration = data.get('timer_duration', 600)  # 10 minutes default

    # Create new game
    board = ChessBoard()
    game = Game(
        user_id=user.id,
        fen=board.to_fen(),
        difficulty=difficulty,
        timer_enabled=timer_enabled,
        timer_duration=timer_duration,
        timer_remaining=timer_duration if timer_enabled else None,
        status='in_progress'
    )

    db.session.add(game)
    db.session.commit()

    return jsonify({
        'message': 'Game started successfully',
        'game': game.to_dict(),
        'board': {
            'fen': game.fen,
            'turn': 'white' if board.turn == 'w' else 'black'
        }
    }), 201

@game_bp.route('/<int:game_id>/move', methods=['POST'])
def make_move(game_id):
    """Make a move in a game"""
    user = get_user_from_token()
    if not user:
        return jsonify({'error': 'Invalid or missing token'}), 401

    game = Game.query.filter_by(id=game_id, user_id=user.id).first()
    if not game:
        return jsonify({'error': 'Game not found'}), 404

    if game.status != 'in_progress':
        return jsonify({'error': 'Game is not in progress'}), 400

    data = request.get_json()
    if not data or 'from' not in data or 'to' not in data:
        return jsonify({'error': 'Move details required'}), 400

    from_square = data['from']
    to_square = data['to']

    # Create board and validate move
    board = ChessBoard(game.fen)

    if not board.is_valid_move(from_square, to_square):
        return jsonify({'error': 'Invalid move'}), 400

    # Make the move
    new_fen = board.make_move(from_square, to_square)

    # Save move to database
    move_count = Move.query.filter_by(game_id=game_id).count()
    piece = board.get_piece(*board.square_to_coords(to_square))
    if piece is None:
        # Get the piece that moved (from original position)
        from_coords = board.square_to_coords(from_square)
        # We need to get the piece before the move, but we already made the move
        # Let's use a temporary board to get the piece
        temp_board = ChessBoard(game.fen)
        piece = temp_board.get_piece(*from_coords)

    move = Move(
        game_id=game_id,
        move_number=move_count + 1,
        from_square=from_square,
        to_square=to_square,
        piece=piece if piece else '',
        fen_after=new_fen
    )
    db.session.add(move)

    # Update game
    game.fen = new_fen

    # Check for game end
    result = board.get_game_result()
    if result:
        game.status = result['status']
        game.result = result.get('winner')

    db.session.commit()

    # If game is still in progress and it's black's turn (bot), make bot move
    if game.status == 'in_progress' and board.turn == 'b':
        from ..services.bot_ai import BotAI
        bot = BotAI(game.difficulty)
        bot_move = bot.get_best_move(board)

        if bot_move:
            # Make bot move
            new_fen = board.make_move(bot_move['from'], bot_move['to'])

            # Save bot move
            move_count += 1
            piece = board.get_piece(*board.square_to_coords(bot_move['to']))
            if piece is None:
                temp_board = ChessBoard(game.fen)
                piece = temp_board.get_piece(*temp_board.square_to_coords(bot_move['from']))

            bot_move_record = Move(
                game_id=game_id,
                move_number=move_count + 1,
                from_square=bot_move['from'],
                to_square=bot_move['to'],
                piece=piece if piece else '',
                fen_after=new_fen
            )
            db.session.add(bot_move_record)

            # Update game
            game.fen = new_fen

            # Check for game end after bot move
            result = board.get_game_result()
            if result:
                game.status = result['status']
                game.result = result.get('winner')

            db.session.commit()

    return jsonify({
        'message': 'Move made successfully',
        'game': game.to_dict(),
        'board': {
            'fen': game.fen,
            'turn': 'white' if board.turn == 'w' else 'black'
        },
        'result': result
    }), 200

@game_bp.route('/<int:game_id>', methods=['GET'])
def get_game(game_id):
    """Get game state"""
    user = get_user_from_token()
    if not user:
        return jsonify({'error': 'Invalid or missing token'}), 401

    game = Game.query.filter_by(id=game_id, user_id=user.id).first()
    if not game:
        return jsonify({'error': 'Game not found'}), 404

    board = ChessBoard(game.fen)

    return jsonify({
        'game': game.to_dict(),
        'board': {
            'fen': game.fen,
            'turn': 'white' if board.turn == 'w' else 'black',
            'valid_moves': board.get_valid_moves('white' if board.turn == 'w' else 'black')
        }
    }), 200

@game_bp.route('/history', methods=['GET'])
def get_game_history():
    """Get user's game history"""
    user = get_user_from_token()
    if not user:
        return jsonify({'error': 'Invalid or missing token'}), 401

    games = Game.query.filter_by(user_id=user.id).order_by(Game.created_at.desc()).all()

    return jsonify({
        'games': [game.to_dict() for game in games]
    }), 200
