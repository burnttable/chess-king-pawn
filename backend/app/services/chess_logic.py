"""
Chess Logic Service - King & Pawn Variant
Implements chess rules for only kings and pawns
"""

class ChessBoard:
    """Chess board representation and logic"""

    # Piece representations
    WHITE_PAWN = 'P'
    WHITE_KING = 'K'
    BLACK_PAWN = 'p'
    BLACK_KING = 'k'
    EMPTY = None

    # Initial FEN for king & pawn variant
    INITIAL_FEN = 'k7/8/8/8/8/8/PPPPPPPP/4K3 w - - 0 1'

    def __init__(self, fen=None):
        """Initialize board from FEN notation"""
        if fen is None:
            fen = self.INITIAL_FEN
        self.load_fen(fen)

    def load_fen(self, fen):
        """Load board state from FEN notation"""
        parts = fen.split()
        board_part = parts[0]

        # Initialize 8x8 board
        self.board = [[None for _ in range(8)] for _ in range(8)]

        # Parse board from FEN
        rows = board_part.split('/')
        for row_idx, row in enumerate(rows):
            col_idx = 0
            for char in row:
                if char.isdigit():
                    # Empty squares
                    col_idx += int(char)
                else:
                    # Piece
                    self.board[row_idx][col_idx] = char
                    col_idx += 1

        # Parse other FEN components
        self.turn = parts[1] if len(parts) > 1 else 'w'

    def to_fen(self):
        """Convert current board state to FEN notation"""
        fen_rows = []

        for row in self.board:
            empty_count = 0
            fen_row = ''

            for square in row:
                if square is None:
                    empty_count += 1
                else:
                    if empty_count > 0:
                        fen_row += str(empty_count)
                        empty_count = 0
                    fen_row += square

            if empty_count > 0:
                fen_row += str(empty_count)

            fen_rows.append(fen_row)

        board_fen = '/'.join(fen_rows)
        return f"{board_fen} {self.turn} - - 0 1"

    def get_piece(self, row, col):
        """Get piece at position"""
        if 0 <= row < 8 and 0 <= col < 8:
            return self.board[row][col]
        return None

    def set_piece(self, row, col, piece):
        """Set piece at position"""
        if 0 <= row < 8 and 0 <= col < 8:
            self.board[row][col] = piece

    def is_white_piece(self, piece):
        """Check if piece is white"""
        return piece in [self.WHITE_PAWN, self.WHITE_KING]

    def is_black_piece(self, piece):
        """Check if piece is black"""
        return piece in [self.BLACK_PAWN, self.BLACK_KING]

    def get_piece_color(self, piece):
        """Get piece color: 'white', 'black', or None"""
        if piece is None:
            return None
        return 'white' if self.is_white_piece(piece) else 'black'

    def find_king(self, color):
        """Find king position for given color"""
        king_piece = self.WHITE_KING if color == 'white' else self.BLACK_KING

        for row in range(8):
            for col in range(8):
                if self.board[row][col] == king_piece:
                    return (row, col)
        return None

    def is_in_check(self, color):
        """Check if king of given color is in check"""
        king_pos = self.find_king(color)
        if king_pos is None:
            return False

        # Check if any opponent piece can capture the king
        opponent_color = 'black' if color == 'white' else 'white'

        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and self.get_piece_color(piece) == opponent_color:
                    # Check if this piece can attack the king
                    if self.can_piece_attack(row, col, king_pos[0], king_pos[1]):
                        return True

        return False

    def can_piece_attack(self, from_row, from_col, to_row, to_col):
        """Check if piece at from_pos can attack to_pos"""
        piece = self.board[from_row][from_col]

        if piece == self.WHITE_PAWN:
            # White pawn attacks diagonally upward
            return (to_row == from_row - 1 and
                    abs(to_col - from_col) == 1)
        elif piece == self.BLACK_PAWN:
            # Black pawn attacks diagonally downward
            return (to_row == from_row + 1 and
                    abs(to_col - from_col) == 1)
        elif piece in [self.WHITE_KING, self.BLACK_KING]:
            # King attacks adjacent squares
            return (abs(to_row - from_row) <= 1 and
                    abs(to_col - from_col) <= 1)

        return False

    def make_move(self, from_square, to_square):
        """Make a move on the board (without validation)"""
        # Convert square notation (e.g., "e2") to coordinates
        from_col = ord(from_square[0]) - ord('a')
        from_row = 8 - int(from_square[1])
        to_col = ord(to_square[0]) - ord('a')
        to_row = 8 - int(to_square[1])

        # Get piece
        piece = self.board[from_row][from_col]

        # Handle pawn promotion
        if piece == self.WHITE_PAWN and to_row == 0:
            piece = 'Q'  # Promote to Queen
        elif piece == self.BLACK_PAWN and to_row == 7:
            piece = 'q'  # Promote to Queen

        # Move piece
        self.board[to_row][to_col] = piece
        self.board[from_row][from_col] = None

        # Switch turn
        self.turn = 'b' if self.turn == 'w' else 'w'

        return self.to_fen()

    def get_pawn_moves(self, row, col):
        """Get all valid pawn moves from position"""
        piece = self.board[row][col]
        moves = []

        if piece == self.WHITE_PAWN:
            # White pawn moves upward (decreasing row)
            # Forward one square
            if row > 0 and self.board[row - 1][col] is None:
                moves.append((row - 1, col))
                # Forward two squares from starting position
                if row == 6 and self.board[row - 2][col] is None:
                    moves.append((row - 2, col))

            # Diagonal captures
            for col_offset in [-1, 1]:
                new_col = col + col_offset
                if 0 <= new_col < 8 and row > 0:
                    target = self.board[row - 1][new_col]
                    if target and self.is_black_piece(target):
                        moves.append((row - 1, new_col))

        elif piece == self.BLACK_PAWN:
            # Black pawn moves downward (increasing row)
            # Forward one square
            if row < 7 and self.board[row + 1][col] is None:
                moves.append((row + 1, col))
                # Forward two squares from starting position
                if row == 1 and self.board[row + 2][col] is None:
                    moves.append((row + 2, col))

            # Diagonal captures
            for col_offset in [-1, 1]:
                new_col = col + col_offset
                if 0 <= new_col < 8 and row < 7:
                    target = self.board[row + 1][new_col]
                    if target and self.is_white_piece(target):
                        moves.append((row + 1, new_col))

        return moves

    def get_king_moves(self, row, col):
        """Get all valid king moves from position"""
        moves = []

        # King can move one square in any direction
        for row_offset in [-1, 0, 1]:
            for col_offset in [-1, 0, 1]:
                if row_offset == 0 and col_offset == 0:
                    continue

                new_row = row + row_offset
                new_col = col + col_offset

                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    target = self.board[new_row][new_col]
                    piece_color = self.get_piece_color(self.board[row][col])

                    # Can move to empty square or capture opponent
                    if target is None or self.get_piece_color(target) != piece_color:
                        moves.append((new_row, new_col))

        return moves

    def get_valid_moves(self, color):
        """Get all valid moves for a color"""
        moves = []

        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and self.get_piece_color(piece) == color:
                    piece_moves = self.get_piece_moves(row, col)
                    for move in piece_moves:
                        # Check if move leaves king in check
                        if not self.leaves_king_in_check(row, col, move[0], move[1], color):
                            from_square = self.coords_to_square(row, col)
                            to_square = self.coords_to_square(move[0], move[1])
                            moves.append({
                                'from': from_square,
                                'to': to_square,
                                'piece': piece
                            })

        return moves

    def get_piece_moves(self, row, col):
        """Get all possible moves for a piece (without check validation)"""
        piece = self.board[row][col]

        if piece == self.WHITE_PAWN or piece == self.BLACK_PAWN:
            return self.get_pawn_moves(row, col)
        elif piece == self.WHITE_KING or piece == self.BLACK_KING:
            return self.get_king_moves(row, col)
        else:
            return []

    def leaves_king_in_check(self, from_row, from_col, to_row, to_col, color):
        """Check if a move would leave the king in check"""
        # Create a copy of the board
        test_board = self.clone()

        # Make the move on the test board
        piece = test_board.board[from_row][from_col]

        # Handle pawn promotion
        if piece == self.WHITE_PAWN and to_row == 0:
            piece = 'Q'
        elif piece == self.BLACK_PAWN and to_row == 7:
            piece = 'q'

        test_board.board[to_row][to_col] = piece
        test_board.board[from_row][from_col] = None

        # Check if king is in check
        return test_board.is_in_check(color)

    def is_valid_move(self, from_square, to_square):
        """Check if a move is valid"""
        # Convert square notation to coordinates
        from_col = ord(from_square[0]) - ord('a')
        from_row = 8 - int(from_square[1])
        to_col = ord(to_square[0]) - ord('a')
        to_row = 8 - int(to_square[1])

        # Check bounds
        if not (0 <= from_row < 8 and 0 <= from_col < 8):
            return False
        if not (0 <= to_row < 8 and 0 <= to_col < 8):
            return False

        # Get piece
        piece = self.board[from_row][from_col]
        if piece is None:
            return False

        # Check if it's the right color's turn
        piece_color = self.get_piece_color(piece)
        turn_color = 'white' if self.turn == 'w' else 'black'
        if piece_color != turn_color:
            return False

        # Get valid moves for this piece
        valid_moves = self.get_piece_moves(from_row, from_col)
        if (to_row, to_col) not in valid_moves:
            return False

        # Check if move leaves king in check
        if self.leaves_king_in_check(from_row, from_col, to_row, to_col, piece_color):
            return False

        return True

    def coords_to_square(self, row, col):
        """Convert coordinates to square notation"""
        file = chr(ord('a') + col)
        rank = 8 - row
        return f"{file}{rank}"

    def square_to_coords(self, square):
        """Convert square notation to coordinates"""
        file = square[0]
        rank = int(square[1])
        col = ord(file) - ord('a')
        row = 8 - rank
        return (row, col)

    def is_checkmate(self, color):
        """Check if the given color is in checkmate"""
        if not self.is_in_check(color):
            return False

        # If in check, check if there are any valid moves
        return len(self.get_valid_moves(color)) == 0

    def is_stalemate(self, color):
        """Check if the given color is in stalemate"""
        if self.is_in_check(color):
            return False

        # If not in check but no valid moves, it's stalemate
        return len(self.get_valid_moves(color)) == 0

    def has_insufficient_material(self):
        """Check if there's insufficient material to checkmate"""
        white_pawns = 0
        black_pawns = 0
        white_king = False
        black_king = False

        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece == self.WHITE_PAWN:
                    white_pawns += 1
                elif piece == self.BLACK_PAWN:
                    black_pawns += 1
                elif piece == self.WHITE_KING:
                    white_king = True
                elif piece == self.BLACK_KING:
                    black_king = True

        # If only kings remain, insufficient material
        if white_king and black_king and white_pawns == 0 and black_pawns == 0:
            return True

        return False

    def get_game_result(self):
        """Get the current game result"""
        turn_color = 'white' if self.turn == 'w' else 'black'

        if self.is_checkmate(turn_color):
            winner = 'black' if turn_color == 'white' else 'white'
            return {'status': 'checkmate', 'winner': winner}

        if self.is_stalemate(turn_color):
            return {'status': 'stalemate', 'winner': None}

        if self.has_insufficient_material():
            return {'status': 'insufficient_material', 'winner': None}

        return None

    def clone(self):
        """Create a deep copy of the board"""
        new_board = ChessBoard(self.to_fen())
        return new_board
