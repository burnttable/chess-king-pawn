/**
 * Game State Manager
 * Manages the game state, timer, and move history
 */

class GameStateManager {
    constructor() {
        this.game = null;
        this.board = null;
        this.currentMoveIndex = 0;
        this.moveHistory = [];
        this.timerInterval = null;
        this.timeRemaining = 0;
        this.onStateChange = null;
        this.onGameOver = null;
        this.onTimerUpdate = null;
    }

    /**
     * Initialize a new game
     */
    initializeGame(gameData) {
        this.game = gameData.game;
        this.board = gameData.board;
        this.moveHistory = [];
        this.currentMoveIndex = 0;

        // Initialize timer if enabled
        if (this.game.timer_enabled) {
            this.timeRemaining = this.game.timer_remaining;
            this.startTimer();
        }

        this.notifyStateChange();
    }

    /**
     * Update game state after a move
     */
    updateState(gameData) {
        this.game = gameData.game;
        this.board = gameData.board;

        this.notifyStateChange();

        // Check for game over
        if (gameData.result) {
            this.handleGameOver(gameData.result);
        }
    }

    /**
     * Add move to history
     */
    addMove(move) {
        this.moveHistory.push(move);
        this.currentMoveIndex++;
    }

    /**
     * Start the timer
     */
    startTimer() {
        this.stopTimer();

        this.timerInterval = setInterval(() => {
            this.timeRemaining--;

            if (this.onTimerUpdate) {
                this.onTimerUpdate(this.timeRemaining);
            }

            if (this.timeRemaining <= 0) {
                this.stopTimer();
                this.handleGameOver({ status: 'timeout', winner: 'black' });
            }
        }, 1000);
    }

    /**
     * Stop the timer
     */
    stopTimer() {
        if (this.timerInterval) {
            clearInterval(this.timerInterval);
            this.timerInterval = null;
        }
    }

    /**
     * Get current game state
     */
    getState() {
        return {
            game: this.game,
            board: this.board,
            moveHistory: this.moveHistory,
            currentMoveIndex: this.currentMoveIndex
        };
    }

    /**
     * Get current turn
     */
    getCurrentTurn() {
        return this.board.turn;
    }

    /**
     * Check if it's player's turn (white)
     */
    isPlayerTurn() {
        return this.getCurrentTurn() === 'white';
    }

    /**
     * Check if game is over
     */
    isGameOver() {
        return this.game.status !== 'in_progress';
    }

    /**
     * Get game result
     */
    getResult() {
        if (this.isGameOver()) {
            return {
                status: this.game.status,
                winner: this.game.result
            };
        }
        return null;
    }

    /**
     * Format time as MM:SS
     */
    formatTime(seconds) {
        const mins = Math.floor(seconds / 60);
        const secs = seconds % 60;
        return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }

    /**
     * Get game status text
     */
    getStatusText() {
        if (this.isGameOver()) {
            return this.game.status.replace('_', ' ');
        }
        return 'in progress';
    }

    /**
     * Get winner text
     */
    getWinnerText() {
        if (this.game.result === 'white') {
            return 'You win!';
        } else if (this.game.result === 'black') {
            return 'Bot wins!';
        }
        return 'Draw!';
    }

    /**
     * Handle game over
     */
    handleGameOver(result) {
        this.stopTimer();

        if (this.onGameOver) {
            this.onGameOver(result);
        }
    }

    /**
     * Reset game state
     */
    reset() {
        this.stopTimer();
        this.game = null;
        this.board = null;
        this.moveHistory = [];
        this.currentMoveIndex = 0;
        this.timeRemaining = 0;
    }

    /**
     * Notify state change listeners
     */
    notifyStateChange() {
        if (this.onStateChange) {
            this.onStateChange(this.getState());
        }
    }

    /**
     * Set state change handler
     */
    onStateChange(handler) {
        this.onStateChange = handler;
    }

    /**
     * Set game over handler
     */
    setOnGameOver(handler) {
        this.onGameOver = handler;
    }

    /**
     * Set timer update handler
     */
    setOnTimerUpdate(handler) {
        this.onTimerUpdate = handler;
    }

    /**
     * Export move history as PGN
     */
    exportPGN() {
        let pgn = '';

        for (let i = 0; i < this.moveHistory.length; i += 2) {
            const moveNumber = Math.floor(i / 2) + 1;
            pgn += `${moveNumber}. ${this.moveHistory[i]}`;

            if (i + 1 < this.moveHistory.length) {
                pgn += ` ${this.moveHistory[i + 1]}`;
            }

            pgn += ' ';
        }

        return pgn;
    }
}
