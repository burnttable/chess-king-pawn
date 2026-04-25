import random
from .chess_logic import ChessBoard

class BotAI:
    """AI opponent for chess game"""

    # Piece-square table for pawn positional evaluation
    PAWN_TABLE = [
        [0,  0,  0,  0,  0,  0,  0,  0],     # 8th rank
        [50, 50, 50, 50, 50, 50, 50, 50],    # 7th rank
        [10, 10, 20, 30, 30, 20, 10, 10],    # 6th rank
        [5,  5, 10, 25, 25, 10,  5,  5],     # 5th rank
        [0,  0,  0, 20, 20,  0,  0,  0],     # 4th rank
        [5, -5,-10,  0,  0,-10, -5,  5],     # 3rd rank
        [5, 10, 10,-20,-20, 10, 10,  5],     # 2nd rank
        [0,  0,  0,  0,  0,  0,  0,  0]      # 1st rank
    ]

    def __init__(self, difficulty):
        """Initialize bot with difficulty level"""
        self.difficulty = difficulty

    def get_best_move(self, board):
        """Get the best move for the current position"""
        if self.difficulty == 'easy':
            return self._get_random_move(board)
        elif self.difficulty == 'medium':
            return self._get_greedy_move(board)
        else:  # hard
            return self._get_minimax_move(board)

    def _get_random_move(self, board):
        """Easy difficulty: random move selection"""
        color = 'black' if board.turn == 'b' else 'white'
        valid_moves = board.get_valid_moves(color)

        if not valid_moves:
            return None

        return random.choice(valid_moves)

    def _get_greedy_move(self, board):
        """Medium difficulty: simple evaluation function"""
        color = 'black' if board.turn == 'b' else 'white'
        valid_moves = board.get_valid_moves(color)

        if not valid_moves:
            return None

        # Evaluate each move
        best_move = None
        best_score = float('-inf')

        for move in valid_moves:
            score = self._evaluate_move(board, move, color)
            if score > best_score:
                best_score = score
                best_move = move

        return best_move

    def _get_minimax_move(self, board):
        """Hard difficulty: minimax with alpha-beta pruning"""
        color = 'black' if board.turn == 'b' else 'white'
        valid_moves = board.get_valid_moves(color)

        if not valid_moves:
            return None

        best_move = None
        best_score = float('-inf')
        depth = 4  # Search depth

        for move in valid_moves:
            # Make move on temporary board
            test_board = board.clone()
            test_board.make_move(move['from'], move['to'])

            # Minimax search
            score = self._minimax(test_board, depth - 1, float('-inf'), float('inf'), False)

            if score > best_score:
                best_score = score
                best_move = move

        return best_move

    def _minimax(self, board, depth, alpha, beta, is_maximizing):
        """Minimax algorithm with alpha-beta pruning"""
        # Check for terminal states
        result = board.get_game_result()
        if result:
            if result['status'] == 'checkmate':
                return 1000 if result['winner'] == 'black' else -1000
            elif result['status'] in ['stalemate', 'insufficient_material']:
                return 0

        if depth == 0:
            return self._evaluate_board(board)

        color = 'black' if board.turn == 'b' else 'white'
        valid_moves = board.get_valid_moves(color)

        if is_maximizing:
            max_score = float('-inf')
            for move in valid_moves:
                test_board = board.clone()
                test_board.make_move(move['from'], move['to'])
                score = self._minimax(test_board, depth - 1, alpha, beta, False)
                max_score = max(max_score, score)
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
            return max_score
        else:
            min_score = float('inf')
            for move in valid_moves:
                test_board = board.clone()
                test_board.make_move(move['from'], move['to'])
                score = self._minimax(test_board, depth - 1, alpha, beta, True)
                min_score = min(min_score, score)
                beta = min(beta, score)
                if beta <= alpha:
                    break
            return min_score

    def _evaluate_move(self, board, move, color):
        """Simple evaluation function for medium difficulty"""
        score = 0

        # Get piece being moved
        from_coords = board.square_to_coords(move['from'])
        to_coords = board.square_to_coords(move['to'])
        piece = board.get_piece(*from_coords)

        # Capture bonus
        target_piece = board.get_piece(*to_coords)
        if target_piece:
            if target_piece == 'P' or target_piece == 'p':
                score += 100  # Captured pawn
            elif target_piece == 'K' or target_piece == 'k':
                score += 1000  # Captured king (shouldn't happen)

        # Pawn advancement
        if piece == 'P':
            score += (7 - from_coords[0]) * 2  # White pawn advancement
        elif piece == 'p':
            score += from_coords[0] * 2  # Black pawn advancement

        # Central control
        if 3 <= to_coords[1] <= 4 and 3 <= to_coords[0] <= 4:
            score += 5

        # Check bonus
        test_board = board.clone()
        test_board.make_move(move['from'], move['to'])
        opponent_color = 'white' if color == 'black' else 'black'
        if test_board.is_in_check(opponent_color):
            score += 50

        return score

    def _evaluate_board(self, board):
        """Evaluate board position for hard difficulty"""
        score = 0

        for row in range(8):
            for col in range(8):
                piece = board.get_piece(row, col)
                if piece:
                    piece_score = self._get_piece_value(piece, row, col)
                    if board.is_black_piece(piece):
                        score += piece_score
                    else:
                        score -= piece_score

        # Mobility bonus
        black_moves = len(board.get_valid_moves('black'))
        white_moves = len(board.get_valid_moves('white'))
        score += (black_moves - white_moves)

        return score

    def _get_piece_value(self, piece, row, col):
        """Get piece value with positional considerations"""
        if piece == 'P':  # White pawn
            # Use pawn table (flipped for white)
            return 100 + self.PAWN_TABLE[7 - row][col]
        elif piece == 'p':  # Black pawn
            return 100 + self.PAWN_TABLE[row][col]
        elif piece == 'K' or piece == 'k':  # Kings
            return 0  # Kings have no material value
        else:  # Promoted queens
            return 900

    def square_to_coords(self, square):
        """Convert square notation to coordinates (for compatibility)"""
        file = square[0]
        rank = int(square[1])
        col = ord(file) - ord('a')
        row = 8 - rank
        return (row, col)
