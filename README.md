# Chess King & Pawn Game 🏆

A fully functional chess variant featuring only kings and pawns, built with Python Flask backend and vanilla JavaScript frontend. Deploy with Cloudflare Pages + Render.com for free hosting!

![Project Status](https://img.shields.io/badge/status-production--ready-success)
![Deployment](https://img.shields.io/badge/deployment-cloudflare--pages--render-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## 🎮 Features

### Core Gameplay
- **Chess Variant**: Kings and pawns only (simplified rules)
- **Bot AI**: Three difficulty levels
  - Easy: Random moves
  - Medium: Greedy evaluation
  - Hard: Minimax with alpha-beta pruning
- **Move Validation**: Complete chess rules implementation
- **Win Detection**: Checkmate, stalemate, insufficient material, timeout

### User Features
- **Username Authentication**: Simple token-based system
- **Settings Persistence**: Save preferences across sessions
- **Light/Dark Themes**: Switch between themes instantly
- **Game Timer**: Optional countdown timer with warnings
- **Move History**: Track all moves in the game
- **Responsive Design**: Works on desktop, tablet, and mobile

## 🚀 Quick Start

### Option 1: Play Locally

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/chess-king-pawn.git
   cd chess-king-pawn
   ```

2. **Start the backend**
   ```bash
   cd backend
   python -m venv venv
   venv\Scripts\activate  # On Windows
   source venv/bin/activate  # On Mac/Linux
   pip install -r requirements.txt
   python run.py
   ```

3. **Open the frontend**
   ```bash
   # In a new terminal
   cd frontend
   python -m http.server 5500
   ```

4. **Play!**
   - Open browser to `http://localhost:5500`
   - Enter username and start playing!

### Option 2: Deploy to Production

See **[DEPLOYMENT.md](DEPLOYMENT.md)** for complete deployment guide.

**Quick summary:**
1. Push to GitHub
2. Deploy backend to [Render.com](https://render.com)
3. Deploy frontend to [Cloudflare Pages](https://pages.cloudflare.com)
4. Done! 🎉

## 📁 Project Structure

```
chess-king-pawn/
├── backend/                    # Flask API Server
│   ├── app/
│   │   ├── models/            # SQLAlchemy database models
│   │   ├── routes/            # API endpoints (auth, game, settings)
│   │   ├── services/          # Chess logic & AI engine
│   │   ├── utils/             # Helper functions
│   │   ├── config.py          # Configuration management
│   │   ├── db.py              # Database initialization
│   │   └── __init__.py        # Flask application factory
│   ├── tests/                 # Comprehensive test suite
│   ├── requirements.txt       # Python dependencies
│   ├── render.yaml           # Render deployment config
│   ├── wsgi.py               # Production WSGI entry point
│   ├── run.py                # Development server
│   └── .env.example          # Environment variables template
├── frontend/                   # Static Web Application
│   ├── css/
│   │   ├── styles.css        # Main stylesheet
│   │   └── themes/           # Light & dark themes
│   ├── js/
│   │   ├── api.js            # API client
│   │   ├── chess.js          # Board renderer
│   │   ├── game-state.js     # State management
│   │   └── app.js            # Main application
│   ├── _headers              # Cloudflare security headers
│   ├── _redirects            # Cloudflare routing rules
│   └── index.html            # HTML structure
├── DEPLOYMENT.md              # Complete deployment guide
├── README.md                  # This file
├── PHASE1_COMPLETE.md         # Backend foundation documentation
├── PHASE2_COMPLETE.md         # Chess logic documentation
├── PHASE4_COMPLETE.md         # Frontend documentation
└── PHASE6_COMPLETE.md         # Deployment configuration
```

## 🎯 API Endpoints

### Authentication
```http
POST /api/auth/register
POST /api/auth/login
```

### Game Management
```http
POST /api/game/start          # Start new game
POST /api/game/<id>/move      # Make a move
GET  /api/game/<id>           # Get game state
GET  /api/game/history        # Get user's games
```

### Settings
```http
GET /api/settings             # Get user settings
PUT /api/settings             # Update settings
```

### Health
```http
GET /api/health               # API health check
```

## ♟️ Game Rules

### Initial Position
- **White**: King on e1, Pawns on a2-h2
- **Black**: King on e8, Pawns on a7-h7
- **FEN**: `k7/8/8/8/8/8/PPPPPPPP/4K3 w - - 0 1`

### Movement Rules
- **Pawns**:
  - Forward one square (or two from starting position)
  - Capture diagonally
  - Promote to Queen on last rank
- **King**:
  - One square in any direction
  - Cannot move into check

### Win Conditions
- Checkmate: King in check with no legal moves
- Stalemate: Not in check but no legal moves
- Insufficient Material: Only kings remain
- Timeout: Timer expires (if enabled)

## 🧪 Development

### Running Tests

```bash
cd backend
pytest tests/ -v
```

**Test Coverage:**
- Chess logic (move validation, check detection)
- Bot AI (all difficulty levels)
- Authentication service
- Database models

### Code Quality

- **Backend**: Python with Flask and SQLAlchemy
- **Frontend**: Vanilla JavaScript (no frameworks)
- **Database**: SQLite with ORM
- **Testing**: pytest with comprehensive coverage

## 🌐 Deployment

### Production Architecture

```
Frontend (Cloudflare Pages) → Backend (Render.com) → Database (SQLite)
         ↓                          ↓                     ↓
    Global CDN              RESTful API          Data Persistence
    Free Hosting            Free Tier             File Storage
```

### Deployment Platforms

- **Frontend**: [Cloudflare Pages](https://pages.cloudflare.com) (Free)
  - Global CDN
  - Automatic HTTPS
  - Git integration

- **Backend**: [Render.com](https://render.com) (Free Tier)
  - Python hosting
  - Automatic deployments
  - Built-in monitoring

### Deployment Steps

See **[DEPLOYMENT.md](DEPLOYMENT.md)** for detailed instructions:

1. Push code to GitHub
2. Deploy backend to Render.com
3. Deploy frontend to Cloudflare Pages
4. Configure CORS
5. Test and launch!

## 🛠️ Tech Stack

### Backend
- **Flask 3.0** - Web framework
- **SQLAlchemy 2.0** - ORM
- **Flask-CORS** - Cross-origin support
- **SQLite** - Database
- **Gunicorn** - Production server

### Frontend
- **Vanilla JavaScript** - No frameworks
- **CSS Grid/Flexbox** - Layout
- **CSS Variables** - Theming
- **Fetch API** - HTTP requests

### DevOps
- **Render.com** - Backend hosting
- **Cloudflare Pages** - Frontend hosting
- **Git/GitHub** - Version control
- **pytest** - Testing framework

## 📊 Features by Phase

### ✅ Phase 1: Backend Foundation
- Flask application structure
- Database models and migrations
- Authentication system
- Settings management
- RESTful API endpoints

### ✅ Phase 2: Chess Logic
- FEN notation parser
- Move validation for kings and pawns
- Check/checkmate detection
- Win condition logic
- Comprehensive test suite

### ✅ Phase 3: Bot AI
- Easy: Random move selection
- Medium: Greedy evaluation
- Hard: Minimax with alpha-beta pruning
- Piece-square tables for positional play

### ✅ Phase 4: Frontend Development
- HTML structure and layouts
- CSS styling with themes
- Chess board rendering
- Game state management
- Interactive controls
- Responsive design

### ✅ Phase 6: Deployment Configuration
- Render.com deployment setup
- Cloudflare Pages configuration
- Production-ready settings
- Comprehensive documentation

## 🎨 Screenshots

### Light Theme
- Clean, modern interface
- Classic chess colors
- Easy on the eyes

### Dark Theme
- Modern dark aesthetic
- Reduced eye strain
- Perfect for evening play

## 📝 Configuration

### Environment Variables

**Backend (.env):**
```bash
FLASK_ENV=development
SECRET_KEY=your-secret-key
FRONTEND_URLS=http://localhost:5500,https://your-frontend.com
DATABASE_URL=sqlite:///chess.db
```

**Frontend:** Auto-detects environment - no configuration needed!

## 🔒 Security

- Token-based authentication
- CORS protection
- Secure session cookies
- Input validation
- SQL injection prevention (ORM)
- XSS protection

## 📈 Performance

- Lightweight frontend (no frameworks)
- Efficient move validation
- Optimized AI algorithms
- Global CDN distribution
- Fast response times

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

MIT License - feel free to use this project for learning or as a base for your own chess game!

## 🙏 Acknowledgments

- Chess rules and FEN notation standards
- Minimax algorithm resources
- Flask and Python communities
- Cloudflare and Render for free hosting

## 📧 Support

- Issues: [GitHub Issues](https://github.com/YOUR_USERNAME/chess-king-pawn/issues)
- Documentation: See `DEPLOYMENT.md` and `PHASE*_COMPLETE.md` files

## 🎉 Status

**✅ Project Complete and Production-Ready!**

All features implemented, tested, and documented. Ready for deployment and play!

---

**Made with ❤️ for chess enthusiasts everywhere**

Start playing: `localhost:5500` or deploy to production!
