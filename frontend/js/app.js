/**
 * Main Application
 * Ties together all modules and handles user interactions
 */

class ChessApp {
    constructor() {
        this.api = window.api;
        this.chessBoard = null;
        this.gameState = null;
        this.currentGameId = null;
        this.userSettings = null;

        this.init();
    }

    /**
     * Initialize the application
     */
    async init() {
        // Initialize modules
        this.chessBoard = new ChessBoard('chess-board');
        this.gameState = new GameStateManager();

        // Set up board click handler
        this.chessBoard.setOnSquareClick((from, to) => this.handleSquareClick(from, to));

        // Set up game state handlers
        this.gameState.setOnTimerUpdate((time) => this.updateTimerDisplay(time));
        this.gameState.setOnGameOver((result) => this.handleGameOver(result));

        // Check for existing session
        if (this.api.isAuthenticated()) {
            await this.loadGameScreen();
        } else {
            this.showLoginScreen();
        }

        // Set up event listeners
        this.setupEventListeners();

        // Load user settings
        await this.loadSettings();
    }

    /**
     * Set up event listeners
     */
    setupEventListeners() {
        // Login form
        document.getElementById('login-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleLogin();
        });

        // New game button
        document.getElementById('new-game-btn').addEventListener('click', () => {
            this.showNewGameModal();
        });

        // Settings button
        document.getElementById('settings-btn').addEventListener('click', () => {
            this.showSettingsModal();
        });

        // Logout button
        document.getElementById('logout-btn').addEventListener('click', () => {
            this.handleLogout();
        });

        // Settings modal
        document.getElementById('close-settings').addEventListener('click', () => {
            this.hideModal('settings-modal');
        });

        document.getElementById('cancel-settings').addEventListener('click', () => {
            this.hideModal('settings-modal');
        });

        document.getElementById('settings-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleSaveSettings();
        });

        // Theme toggle
        document.getElementById('theme-select').addEventListener('change', (e) => {
            this.handleThemeChange(e.target.value);
        });

        // Timer checkbox
        document.getElementById('timer-enabled').addEventListener('change', (e) => {
            const timerGroup = document.getElementById('timer-duration-group');
            timerGroup.classList.toggle('hidden', !e.target.checked);
        });

        // New game modal
        document.getElementById('close-new-game').addEventListener('click', () => {
            this.hideModal('new-game-modal');
        });

        document.getElementById('cancel-new-game').addEventListener('click', () => {
            this.hideModal('new-game-modal');
        });

        document.getElementById('new-game-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleStartNewGame();
        });

        // Game timer checkbox
        document.getElementById('game-timer-enabled').addEventListener('change', (e) => {
            const timerGroup = document.getElementById('game-timer-duration-group');
            timerGroup.classList.toggle('hidden', !e.target.checked);
        });

        // Game over modal
        document.getElementById('close-game-over').addEventListener('click', () => {
            this.hideModal('game-over-modal');
        });

        document.getElementById('play-again-btn').addEventListener('click', () => {
            this.hideModal('game-over-modal');
            this.showNewGameModal();
        });

        // Game controls
        document.getElementById('resign-btn').addEventListener('click', () => {
            this.handleResign();
        });
    }

    /**
     * Show login screen
     */
    showLoginScreen() {
        document.getElementById('login-screen').classList.remove('hidden');
        document.getElementById('game-screen').classList.add('hidden');
    }

    /**
     * Show game screen
     */
    showGameScreen() {
        document.getElementById('login-screen').classList.add('hidden');
        document.getElementById('game-screen').classList.remove('hidden');
    }

    /**
     * Handle user login/registration
     */
    async handleLogin() {
        const username = document.getElementById('username').value.trim();

        if (!username) {
            alert('Please enter a username');
            return;
        }

        this.showLoading();

        try {
            // Try to login first, if that fails, register
            try {
                await this.api.login(username);
            } catch (error) {
                await this.api.register(username);
            }

            await this.loadGameScreen();
        } catch (error) {
            alert(error.message || 'Login failed');
        } finally {
            this.hideLoading();
        }
    }

    /**
     * Load game screen
     */
    async loadGameScreen() {
        this.showGameScreen();

        const user = this.api.getCurrentUser();
        document.getElementById('user-display').textContent = `Playing as: ${user.username}`;

        // Load user settings
        await this.loadSettings();

        // Show new game modal
        this.showNewGameModal();
    }

    /**
     * Handle logout
     */
    handleLogout() {
        this.api.logout();
        this.gameState.reset();
        this.showLoginScreen();
    }

    /**
     * Load user settings
     */
    async loadSettings() {
        try {
            const settings = await this.api.getSettings();
            this.userSettings = settings.settings || settings;

            // Apply theme
            this.applyTheme(this.userSettings.theme);

            // Update settings form
            document.getElementById('theme-select').value = this.userSettings.theme;
            document.getElementById('difficulty-select').value = this.userSettings.default_difficulty;
            document.getElementById('timer-enabled').checked = this.userSettings.timer_enabled;
            document.getElementById('timer-duration').value = this.userSettings.default_timer_duration / 60;

            // Show/hide timer duration
            const timerGroup = document.getElementById('timer-duration-group');
            timerGroup.classList.toggle('hidden', !this.userSettings.timer_enabled);
        } catch (error) {
            console.error('Failed to load settings:', error);
        }
    }

    /**
     * Handle save settings
     */
    async handleSaveSettings() {
        const settings = {
            theme: document.getElementById('theme-select').value,
            default_difficulty: document.getElementById('difficulty-select').value,
            timer_enabled: document.getElementById('timer-enabled').checked,
            default_timer_duration: parseInt(document.getElementById('timer-duration').value) * 60
        };

        this.showLoading();

        try {
            await this.api.updateSettings(settings);
            this.userSettings = { ...this.userSettings, ...settings };
            this.hideModal('settings-modal');
        } catch (error) {
            alert('Failed to save settings: ' + error.message);
        } finally {
            this.hideLoading();
        }
    }

    /**
     * Handle theme change
     */
    handleThemeChange(theme) {
        this.applyTheme(theme);
    }

    /**
     * Apply theme
     */
    applyTheme(theme) {
        const themeLink = document.getElementById('theme-link');
        themeLink.href = `css/themes/${theme}.css`;
    }

    /**
     * Show settings modal
     */
    showSettingsModal() {
        document.getElementById('settings-modal').classList.remove('hidden');
    }

    /**
     * Show new game modal
     */
    showNewGameModal() {
        // Set default values from user settings
        document.getElementById('game-difficulty').value = this.userSettings?.default_difficulty || 'medium';
        document.getElementById('game-timer-enabled').checked = this.userSettings?.timer_enabled || false;
        document.getElementById('game-timer-duration').value = (this.userSettings?.default_timer_duration || 600) / 60;

        // Show/hide timer duration
        const timerGroup = document.getElementById('game-timer-duration-group');
        timerGroup.classList.toggle('hidden', !this.userSettings?.timer_enabled);

        document.getElementById('new-game-modal').classList.remove('hidden');
    }

    /**
     * Handle start new game
     */
    async handleStartNewGame() {
        const difficulty = document.getElementById('game-difficulty').value;
        const timerEnabled = document.getElementById('game-timer-enabled').checked;
        const timerDuration = parseInt(document.getElementById('game-timer-duration').value) * 60;

        this.hideModal('new-game-modal');
        this.showLoading();

        try {
            const gameData = await this.api.startGame({
                difficulty,
                timer_enabled: timerEnabled,
                timer_duration: timerDuration
            });

            this.currentGameId = gameData.game.id;
            this.gameState.initializeGame(gameData);

            this.updateGameDisplay();
            this.hideModal('game-over-modal');
        } catch (error) {
            alert('Failed to start game: ' + error.message);
        } finally {
            this.hideLoading();
        }
    }

    /**
     * Handle square click
     */
    async handleSquareClick(from, to) {
        if (!this.gameState.isPlayerTurn()) {
            return; // Not player's turn
        }

        if (to) {
            // Make a move
            await this.makeMove(from, to);
        } else {
            // Select square and show valid moves
            const gameData = await this.api.getGame(this.currentGameId);
            const validMoves = gameData.board.valid_moves || [];

            const myValidMoves = validMoves.filter(move => move.from === from);

            this.chessBoard.selectSquare(from);
            this.chessBoard.highlightMoves(myValidMoves);
        }
    }

    /**
     * Make a move
     */
    async makeMove(from, to) {
        this.showLoading();
        this.chessBoard.clearSelection();

        try {
            const gameData = await this.api.makeMove(this.currentGameId, from, to);

            this.gameState.updateState(gameData);
            this.updateGameDisplay();
        } catch (error) {
            alert('Invalid move: ' + error.message);
            this.updateGameDisplay();
        } finally {
            this.hideLoading();
        }
    }

    /**
     * Update game display
     */
    updateGameDisplay() {
        const state = this.gameState.getState();

        // Update board
        const gameData = await this.api.getGame(this.currentGameId);
        const validMoves = this.gameState.isPlayerTurn() ? (gameData.board.valid_moves || []) : [];

        this.chessBoard.render(
            state.board.fen,
            validMoves,
            this.getLastMove(),
            this.getCheckSquare()
        );

        // Update game info
        document.getElementById('difficulty-display').textContent = this.gameState.game.difficulty;
        document.getElementById('game-status').textContent = this.gameState.getStatusText();
        document.getElementById('turn-display').textContent = this.gameState.getCurrentTurn();

        // Update timer display
        if (this.gameState.game.timer_enabled) {
            document.getElementById('timer-container').classList.remove('hidden');
            this.updateTimerDisplay(this.gameState.timeRemaining);
        } else {
            document.getElementById('timer-container').classList.add('hidden');
        }

        // Update move history
        this.updateMoveHistory();
    }

    /**
     * Get last move
     */
    getLastMove() {
        const moves = this.gameState.moveHistory;
        return moves.length > 0 ? moves[moves.length - 1] : null;
    }

    /**
     * Get check square
     */
    getCheckSquare() {
        // This would need to be determined from the board state
        // For now, return null
        return null;
    }

    /**
     * Update move history display
     */
    updateMoveHistory() {
        const historyContainer = document.getElementById('move-history');
        historyContainer.innerHTML = '';

        // Get move history from API
        this.api.getGameHistory().then(data => {
            const currentGame = data.games.find(g => g.id === this.currentGameId);
            if (currentGame && currentGame.moves) {
                currentGame.moves.forEach((move, index) => {
                    const moveEntry = document.createElement('div');
                    moveEntry.className = 'move-entry';
                    moveEntry.textContent = `${Math.floor(index / 2) + 1}. ${move.from_square} -> ${move.to_square}`;
                    historyContainer.appendChild(moveEntry);
                });
            }
        }).catch(err => {
            console.error('Failed to load move history:', err);
        });
    }

    /**
     * Update timer display
     */
    updateTimerDisplay(seconds) {
        const timerDisplay = document.getElementById('timer-display');
        timerDisplay.textContent = this.gameState.formatTime(seconds);

        // Add warning class if low time
        if (seconds <= 60) {
            timerDisplay.classList.add('timer-warning');
        } else {
            timerDisplay.classList.remove('timer-warning');
        }
    }

    /**
     * Handle game over
     */
    handleGameOver(result) {
        let message = '';

        switch (result.status) {
            case 'checkmate':
                message = `Checkmate! ${this.gameState.getWinnerText()}`;
                break;
            case 'stalemate':
                message = 'Stalemate! It\'s a draw.';
                break;
            case 'insufficient_material':
                message = 'Insufficient material! It\'s a draw.';
                break;
            case 'timeout':
                message = `Time's up! ${this.gameState.getWinnerText()}`;
                break;
            default:
                message = 'Game Over!';
        }

        document.getElementById('game-over-title').textContent = 'Game Over';
        document.getElementById('game-over-message').textContent = message;
        document.getElementById('game-over-modal').classList.remove('hidden');

        this.chessBoard.showGameOver(message);
    }

    /**
     * Handle resign
     */
    async handleResign() {
        if (confirm('Are you sure you want to resign?')) {
            this.handleGameOver({ status: 'resignation', winner: 'black' });
        }
    }

    /**
     * Hide modal
     */
    hideModal(modalId) {
        document.getElementById(modalId).classList.add('hidden');
    }

    /**
     * Show loading spinner
     */
    showLoading() {
        document.getElementById('loading').classList.remove('hidden');
    }

    /**
     * Hide loading spinner
     */
    hideLoading() {
        document.getElementById('loading').classList.add('hidden');
    }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.app = new ChessApp();
});
