/**
 * API Client for Chess Game
 * Handles all communication with the backend API
 */

// Auto-detect environment and use appropriate API URL
const isProduction = window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1';
const apiURL = isProduction
    ? 'https://chess-backend.onrender.com/api'  // Replace with your Render backend URL
    : 'http://localhost:5000/api';

class ChessAPI {
    constructor(baseURL = apiURL) {
        this.baseURL = baseURL;
        this.token = localStorage.getItem('chess_token');
        this.user = JSON.parse(localStorage.getItem('chess_user')) || null;
    }

    /**
     * Set authentication token
     */
    setToken(token) {
        this.token = token;
        localStorage.setItem('chess_token', token);
    }

    /**
     * Set user data
     */
    setUser(user) {
        this.user = user;
        localStorage.setItem('chess_user', JSON.stringify(user));
    }

    /**
     * Clear authentication data
     */
    clearAuth() {
        this.token = null;
        this.user = null;
        localStorage.removeItem('chess_token');
        localStorage.removeItem('chess_user');
    }

    /**
     * Get authorization headers
     */
    getHeaders() {
        const headers = {
            'Content-Type': 'application/json'
        };

        if (this.token) {
            headers['Authorization'] = `Bearer ${this.token}`;
        }

        return headers;
    }

    /**
     * Make API request
     */
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            ...options,
            headers: {
                ...this.getHeaders(),
                ...options.headers
            }
        };

        try {
            const response = await fetch(url, config);
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Request failed');
            }

            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    /**
     * Register new user
     */
    async register(username) {
        const data = await this.request('/auth/register', {
            method: 'POST',
            body: JSON.stringify({ username })
        });

        this.setToken(data.user.token);
        this.setUser(data.user);

        return data;
    }

    /**
     * Login user
     */
    async login(username) {
        const data = await this.request('/auth/login', {
            method: 'POST',
            body: JSON.stringify({ username })
        });

        this.setToken(data.user.token);
        this.setUser(data.user);

        return data;
    }

    /**
     * Logout user
     */
    logout() {
        this.clearAuth();
    }

    /**
     * Get user settings
     */
    async getSettings() {
        return await this.request('/settings');
    }

    /**
     * Update user settings
     */
    async updateSettings(settings) {
        return await this.request('/settings', {
            method: 'PUT',
            body: JSON.stringify(settings)
        });
    }

    /**
     * Start new game
     */
    async startGame(options = {}) {
        const {
            difficulty = 'medium',
            timer_enabled = false,
            timer_duration = 600
        } = options;

        return await this.request('/game/start', {
            method: 'POST',
            body: JSON.stringify({
                difficulty,
                timer_enabled,
                timer_duration
            })
        });
    }

    /**
     * Make a move
     */
    async makeMove(gameId, from, to) {
        return await this.request(`/game/${gameId}/move`, {
            method: 'POST',
            body: JSON.stringify({ from, to })
        });
    }

    /**
     * Get game state
     */
    async getGame(gameId) {
        return await this.request(`/game/${gameId}`);
    }

    /**
     * Get game history
     */
    async getGameHistory() {
        return await this.request('/game/history');
    }

    /**
     * Health check
     */
    async healthCheck() {
        return await this.request('/health');
    }

    /**
     * Check if user is authenticated
     */
    isAuthenticated() {
        return !!this.token;
    }

    /**
     * Get current user
     */
    getCurrentUser() {
        return this.user;
    }
}

// Create global API instance
const api = new ChessAPI();
