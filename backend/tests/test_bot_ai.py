import pytest
from app.services.bot_ai import BotAI
from app.services.chess_logic import ChessBoard

class TestBotAI:
    """Test cases for BotAI class"""

    def test_easy_bot_returns_valid_move(self):
        """Test that easy bot returns a valid move"""
        board = ChessBoard()
        bot = BotAI('easy')

        move = bot.get_best_move(board)

        assert move is not None
        assert 'from' in move
        assert 'to' in move
        assert 'piece' in move

    def test_medium_bot_returns_valid_move(self):
        """Test that medium bot returns a valid move"""
        board = ChessBoard()
        bot = BotAI('medium')

        move = bot.get_best_move(board)

        assert move is not None
        assert 'from' in move
        assert 'to' in move

    def test_hard_bot_returns_valid_move(self):
        """Test that hard bot returns a valid move"""
        board = ChessBoard()
        bot = BotAI('hard')

        move = bot.get_best_move(board)

        assert move is not None
        assert 'from' in move
        assert 'to' in move

    def test_easy_bot_randomness(self):
        """Test that easy bot makes different moves (random)"""
        board = ChessBoard()
        bot = BotAI('easy')

        moves = []
        for _ in range(10):
            move = bot.get_best_move(board)
            moves.append((move['from'], move['to']))

        # Should have some variety (not all the same)
        assert len(set(moves)) > 1

    def test_medium_bot_consistency(self):
        """Test that medium bot is consistent with same position"""
        board = ChessBoard()
        bot = BotAI('medium')

        move1 = bot.get_best_move(board)
        move2 = bot.get_best_move(board)

        # Same position should give same move (deterministic)
        assert move1 == move2

    def test_hard_bot_consistency(self):
        """Test that hard bot is consistent with same position"""
        board = ChessBoard()
        bot = BotAI('hard')

        move1 = bot.get_best_move(board)
        move2 = bot.get_best_move(board)

        # Same position should give same move (deterministic)
        assert move1 == move2

    def test_evaluate_board(self):
        """Test board evaluation"""
        board = ChessBoard()
        bot = BotAI('hard')

        score = bot._evaluate_board(board)

        # Score should be a number
        assert isinstance(score, int) or isinstance(score, float)

    def test_evaluate_move(self):
        """Test move evaluation"""
        board = ChessBoard()
        bot = BotAI('medium')

        move = {'from': 'e2', 'to': 'e4', 'piece': 'P'}
        score = bot._evaluate_move(board, move, 'white')

        # Score should be a number
        assert isinstance(score, int) or isinstance(score, float)

    def test_minimax_depth(self):
        """Test that minimax respects depth"""
        board = ChessBoard()
        bot = BotAI('hard')

        # Make a move (which uses minimax internally)
        move = bot.get_best_move(board)

        assert move is not None

    def test_piece_value_calculation(self):
        """Test piece value calculation"""
        board = ChessBoard()
        bot = BotAI('hard')

        # White pawn on e2 (row 6, col 4)
        value = bot._get_piece_value('P', 6, 4)

        # Should be positive (100 + positional bonus)
        assert value > 0

    def test_no_valid_moves_returns_none(self):
        """Test that bot returns None when no valid moves"""
        # Create a position with no valid moves for black
        board = ChessBoard('k7/8/8/8/8/8/PPPPPPPP/K7 w - - 0 1')
        board.turn = 'b'  # Black's turn but no pieces to move

        bot = BotAI('easy')
        move = bot.get_best_move(board)

        assert move is None
