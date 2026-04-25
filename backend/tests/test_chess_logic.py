import pytest
from app.services.chess_logic import ChessBoard

class TestChessBoard:
    """Test cases for ChessBoard class"""

    def test_initial_board_setup(self):
        """Test initial board setup"""
        board = ChessBoard()

        # Check white pawns on row 6 (a2-h2 in chess notation)
        for col in range(8):
            assert board.board[6][col] == 'P'

        # Check black pawns on row 1 (a7-h7 in chess notation)
        for col in range(8):
            assert board.board[1][col] == 'p'

        # Check white king on e1 (row 7, col 4)
        assert board.board[7][4] == 'K'

        # Check black king on e8 (row 0, col 4)
        assert board.board[0][4] == 'k'

    def test_fen_parsing(self):
        """Test FEN notation parsing"""
        board = ChessBoard('k7/8/8/8/8/8/PPPPPPPP/4K3 w - - 0 1')

        assert board.turn == 'w'
        assert board.board[7][4] == 'K'
        assert board.board[0][4] == 'k'

    def test_fen_generation(self):
        """Test FEN notation generation"""
        board = ChessBoard()
        fen = board.to_fen()

        assert 'k7/8/8/8/8/8/PPPPPPPP/4K3' in fen
        assert 'w' in fen

    def test_pawn_forward_move(self):
        """Test pawn forward movement"""
        board = ChessBoard()

        # White pawn can move forward from e2
        from_coords = (6, 4)  # e2
        to_coords = (5, 4)    # e3

        moves = board.get_pawn_moves(*from_coords)
        assert to_coords in moves

    def test_pawn_double_move_from_start(self):
        """Test pawn double move from starting position"""
        board = ChessBoard()

        # White pawn can move two squares from e2
        from_coords = (6, 4)  # e2
        to_coords = (4, 4)    # e4

        moves = board.get_pawn_moves(*from_coords)
        assert to_coords in moves

    def test_king_movement(self):
        """Test king movement"""
        board = ChessBoard()

        # White king can move in all directions
        from_coords = (7, 4)  # e1

        moves = board.get_king_moves(*from_coords)

        # Should be able to move to adjacent squares
        assert (7, 3) in moves  # d1
        assert (7, 5) in moves  # f1
        assert (6, 4) in moves  # e2
        assert (6, 3) in moves  # d2
        assert (6, 5) in moves  # f2

    def test_is_in_check(self):
        """Test check detection"""
        # Setup a position where white king is in check
        board = ChessBoard('k7/8/8/8/8/4p3/8/4K3 w - - 0 1')

        # White king should be in check from black pawn
        assert board.is_in_check('white')

    def test_valid_move_detection(self):
        """Test valid move detection"""
        board = ChessBoard()

        # Get valid moves for white
        moves = board.get_valid_moves('white')

        # Should have pawn moves
        assert len(moves) > 0

        # All moves should be from white pieces
        for move in moves:
            assert board.is_white_piece(move['piece'])

    def test_invalid_move(self):
        """Test invalid move detection"""
        board = ChessBoard()

        # Try to move from empty square
        assert not board.is_valid_move('e4', 'e5')

        # Try to move opponent's piece
        assert not board.is_valid_move('e7', 'e6')

    def test_move_execution(self):
        """Test move execution"""
        board = ChessBoard()
        original_turn = board.turn

        # Make a move
        new_fen = board.make_move('e2', 'e4')

        # Check that turn changed
        assert board.turn != original_turn

        # Check that pawn moved
        assert board.board[4][4] == 'P'  # e4
        assert board.board[6][4] is None  # e2 should be empty

    def test_checkmate_detection(self):
        """Test checkmate detection"""
        # Create a checkmate position
        board = ChessBoard('k7/8/8/8/8/8/PPPPPPPP/K7 w - - 0 1')

        # This should not be checkmate
        assert not board.is_checkmate('white')

    def test_stalemate_detection(self):
        """Test stalemate detection"""
        board = ChessBoard()

        # Initial position is not stalemate
        assert not board.is_stalemate('white')

    def test_insufficient_material(self):
        """Test insufficient material detection"""
        # Position with only kings
        board = ChessBoard('k7/8/8/8/8/8/8/4K3 w - - 0 1')

        assert board.has_insufficient_material()

    def test_pawn_capture(self):
        """Test pawn capture"""
        # Setup a capture position
        board = ChessBoard('k7/8/8/8/8/4p3/8/4K3 w - - 0 1')

        # White pawn can capture black pawn
        from_coords = (6, 3)  # d2
        moves = board.get_pawn_moves(*from_coords)

        # Should include capture
        assert (5, 4) in moves  # capture on e3

    def test_square_conversion(self):
        """Test square notation conversion"""
        board = ChessBoard()

        # Convert coordinates to square
        square = board.coords_to_square(7, 4)
        assert square == 'e1'

        # Convert square to coordinates
        coords = board.square_to_coords('e1')
        assert coords == (7, 4)

    def test_board_clone(self):
        """Test board cloning"""
        board = ChessBoard()
        cloned_board = board.clone()

        # Make move on original
        board.make_move('e2', 'e4')

        # Clone should be unchanged
        assert cloned_board.board[6][4] == 'P'  # e2
        assert cloned_board.board[4][4] is None  # e4

        # Original should be changed
        assert board.board[6][4] is None  # e2
        assert board.board[4][4] == 'P'  # e4
