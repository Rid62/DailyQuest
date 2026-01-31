# DailyQuest - Gamified Daily Challenge App

A Flask-based web application that delivers daily challenges across multiple categories to help users build healthy habits and track their progress.

## Features

### Core Functionality
- **Daily Challenges**: Receive one challenge per day from 5 categories:
  - 🎨 Creative (drawing, writing, photography, design)
  - 📚 Learning (articles, facts, code practice)
  - 👥 Social (helping, friend calls)
  - 💪 Sports/Health (exercises, walks, hydration)

- **User Authentication**: Secure login and registration system

- **Gamification System**:
  - Points for completing challenges
  - Level progression
  - Daily streak tracking
  - Badges and achievements

- **Dashboard**:
  - Today's challenge display
  - Personal statistics
  - Progress charts (Chart.js)
  - Badge display

- **Leaderboard**: Compete with other users based on points

- **Achievement Tracking**: View completed challenges and earned badges

## Installation

### Requirements
- Python 3.8+
- pip

### Setup Steps

1. **Clone/Navigate to project directory**:
   ```bash
   cd FINAL_PROJECT
   ```

2. **Create virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Access the app**:
   - Open browser and navigate to: `http://localhost:5000`
   - Register a new account
   - Start completing daily challenges!

## Project Structure

```
FINAL_PROJECT/
├── app.py                 # Flask app + database models
├── requirements.txt       # Python dependencies
├── static/
│   ├── style.css         # All styling
│   └── script.js         # JavaScript utilities
└── templates/
    ├── base.html         # Base template with navbar
    ├── login.html        # Login page
    ├── register.html     # Registration page
    ├── dashboard.html    # Main dashboard
    ├── achievements.html # Achievements page
    └── leaderboard.html  # Leaderboard page
```

## How to Use

1. **Sign Up**: Create a new account with username, email, and password
2. **View Challenge**: Your daily challenge appears on the dashboard
3. **Complete Challenge**: Read the challenge and click "Mark as Complete"
4. **Earn Points**: Get points and see your stats update
5. **Track Progress**: View charts, badges, and leaderboard position
6. **Build Streaks**: Complete challenges daily to build a streak

## Technology Stack

- **Backend**: Python Flask + SQLAlchemy ORM
- **Database**: SQLite (auto-created on first run)
- **Frontend**: HTML, CSS, Vanilla JavaScript
- **Visualization**: Chart.js
- **Authentication**: Flask-Login + Werkzeug hashing

## Features Overview

### Authentication
- Secure password hashing
- Session management
- Login/logout/register

### Challenge System
- Daily challenge assignment
- Category-based selection
- User preference support

### Points & Progression
- Dynamic point calculation
- Automatic level-up system
- Streak calculation

### Badges & Achievements
- Automatic badge awarding:
  - **Dedicated**: 10 challenge completions
  - **On Fire**: 7-day streak
  - **Rising Star**: Reach Level 5

### Charts & Analytics
- Daily completion history
- Points by category breakdown
- Progress visualization

### Leaderboard
- Top 50 users ranking
- Personal rank display
- Real-time updates

## Customization

### Change Secret Key (Important for Production)
In `app.py`, change:
```python
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
```

### Add More Challenges
Edit the `init_db()` function in `app.py` to add custom challenges:
```python
Challenge(
    title='Your challenge title',
    description='What to do',
    category='creative',  # or learning, social, sports
    points=10
)
```

### Customize Badges
Modify the `check_and_award_badges()` function to create custom badge conditions.

## Future Enhancements

- Email notifications for daily challenges
- Push notifications
- Social sharing features
- AI-powered challenge suggestions
- Mobile app
- User profiles
- Challenge difficulty levels
- Custom challenges

## Troubleshooting

**Database Issues**:
- Delete `dailyquest.db` to reset database
- Run `app.py` again to reinitialize

**Import Errors**:
- Ensure all packages from `requirements.txt` are installed
- Check Python version compatibility

**Port Already in Use**:
- Change port in last line of `app.py`:
```python
app.run(debug=True, port=5001)  # Use different port
```

## License

Open source - feel free to modify and use!

## Support

For issues or questions, check the code comments in `app.py` for detailed explanations of each system.

---

**Happy questing! May your streaks be legendary! ⚔️⭐**

## Language Selection

The web UI supports English and Arabic. Use the language selector in the top-right of the navbar to switch languages; your preference is saved in your browser.
