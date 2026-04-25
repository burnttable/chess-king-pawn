/**
 * Chess Board Renderer
 * Handles rendering of the chess board and pieces
 */

class ChessBoard {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.selectedSquare = null;
        this.validMoves = [];
        this.boardState = null;
        this.onSquareClick = null;
        this.lastMove = null;
        this.checkSquare = null;
    }

    /**
     * Unicode chess pieces
     */
    static PIECES = {
        'K': '♔', // White king
        'Q': '♕', // White queen (promoted pawn)
        'P': '♙', // White pawn
        'k': '♚', // Black king
        'q': '♛', // Black queen (promoted pawn)
        'p': '♟'  // Black pawn
    };

    /**
     * Parse FEN and create board array
     */
    parseFEN(fen) {
        const board = [];
        const fenBoard = fen.split(' ')[0];
        const rows = fenBoard.split('/');

        for (const row of rows) {
            const boardRow = [];
            for (const char of row) {
                if (isNaN(char)) {
                    boardRow.push(char);
                } else {
                    for (let i = 0; i < parseInt(char); i++) {
                        boardRow.push(null);
                    }
                }
            }
            board.push(boardRow);
        }

        return board;
    }

    /**
     * Render the chess board
     */
    render(fen, validMoves = [], lastMove = null, checkSquare = null) {
        this.boardState = this.parseFEN(fen);
        this.validMoves = validMoves;
        this.lastMove = lastMove;
        this.checkSquare = checkSquare;
        this.selectedSquare = null;

        this.container.innerHTML = '';
        this.createBoard();
    }

    /**
     * Create board HTML
     */
    createBoard() {
        const files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'];

        for (let row = 0; row < 8; row++) {
            for (let col = 0; col < 8; col++) {
                const square = document.createElement('div');
                const isLight = (row + col) % 2 === 0;
                const squareName = `${files[col]}${8 - row}`;

                square.className = `square ${isLight ? 'light' : 'dark'}`;
                square.dataset.square = squareName;

                // Add piece if present
                const piece = this.boardState[row][col];
                if (piece) {
                    const pieceSpan = document.createElement('span');
                    pieceSpan.className = 'piece';
                    pieceSpan.textContent = ChessBoard.PIECES[piece] || piece;
                    square.appendChild(pieceSpan);
                }

                // Highlight selected square
                if (this.selectedSquare === squareName) {
                    square.classList.add('selected');
                }

                // Highlight valid moves
                const isValidMove = this.validMoves.some(move => move.to === squareName);
                if (isValidMove) {
                    const targetPiece = this.boardState[row][col];
                    if (targetPiece) {
                        square.classList.add('valid-capture');
                    } else {
                        square.classList.add('valid-move');
                    }
                }

                // Highlight last move
                if (this.lastMove) {
                    if (squareName === this.lastMove.from || squareName === this.lastMove.to) {
                        square.classList.add('last-move');
                    }
                }

                // Highlight king in check
                if (this.checkSquare === squareName) {
                    square.classList.add('check');
                }

                // Add coordinates
                if (col === 0) {
                    const rank = document.createElement('span');
                    rank.className = 'coordinate rank';
                    rank.textContent = 8 - row;
                    square.appendChild(rank);
                }
                if (row === 7) {
                    const file = document.createElement('span');
                    file.className = 'coordinate file';
                    file.textContent = files[col];
                    square.appendChild(file);
                }

                // Add click handler
                square.addEventListener('click', () => this.handleSquareClick(squareName));

                this.container.appendChild(square);
            }
        }
    }

    /**
     * Handle square click
     */
    handleSquareClick(squareName) {
        if (!this.onSquareClick) return;

        // If clicking on a valid move, execute it
        const isValidMove = this.validMoves.some(move => move.to === squareName);
        if (isValidMove && this.selectedSquare) {
            this.onSquareClick(this.selectedSquare, squareName);
            this.selectedSquare = null;
            return;
        }

        // Select the square
        this.selectedSquare = squareName;
        this.onSquareClick(squareName);
    }

    /**
     * Get piece at square
     */
    getPieceAt(square) {
        const files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'];
        const col = files.indexOf(square[0]);
        const row = 8 - parseInt(square[1]);

        return this.boardState[row][col];
    }

    /**
     * Clear selection
     */
    clearSelection() {
        this.selectedSquare = null;
        this.validMoves = [];

        const squares = this.container.querySelectorAll('.square');
        squares.forEach(square => {
            square.classList.remove('selected', 'valid-move', 'valid-capture');
        });
    }

    /**
     * Highlight valid moves for a square
     */
    highlightMoves(moves) {
        this.clearSelection();
        this.validMoves = moves;

        moves.forEach(move => {
            const square = this.container.querySelector(`[data-square="${move.to}"]`);
            if (square) {
                const piece = this.getPieceAt(move.to);
                if (piece) {
                    square.classList.add('valid-capture');
                } else {
                    square.classList.add('valid-move');
                }
            }
        });
    }

    /**
     * Select a square
     */
    selectSquare(squareName) {
        this.clearSelection();
        this.selectedSquare = squareName;

        const square = this.container.querySelector(`[data-square="${squareName}"]`);
        if (square) {
            square.classList.add('selected');
        }
    }

    /**
     * Show game over message
     */
    showGameOver(message) {
        const messageDiv = document.getElementById('game-message');
        if (messageDiv) {
            messageDiv.textContent = message;
            messageDiv.classList.remove('hidden');
        }
    }

    /**
     * Hide game over message
     */
    hideGameOver() {
        const messageDiv = document.getElementById('game-message');
        if (messageDiv) {
            messageDiv.classList.add('hidden');
        }
    }

    /**
     * Set click handler
     */
    setOnSquareClick(handler) {
        this.onSquareClick = handler;
    }
}
