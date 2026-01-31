# DailyQuest - Quick Start Guide

## Installation & Running

### Step 1: Install Dependencies
```bash
cd FINAL_PROJECT
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
python app.py
```

### Step 3: Open in Browser
Navigate to: **http://localhost:5000**

---

## First Time Use

1. **Register** - Create an account with username, email, and password
2. **Login** - Use your credentials to log in
3. **Dashboard** - See today's challenge
4. **Complete** - Click "Mark as Complete" to earn points
5. **Track Progress** - View stats, charts, and leaderboard

---

## App Features

✅ **Daily Challenges** - One challenge per day from 4 categories
✅ **User Authentication** - Secure login/register
✅ **Point System** - Earn points and level up
✅ **Streaks** - Track consecutive daily completions
✅ **Badges** - Unlock achievements
✅ **Dashboard** - View progress charts
✅ **Leaderboard** - Compete with other users
✅ **Responsive Design** - Works on desktop and mobile

---

## File Structure

```
FINAL_PROJECT/
├── app.py              # Main Flask application with all logic
├── requirements.txt    # Python packages to install
├── README.md          # Full documentation
├── static/
│   ├── style.css      # All styling
│   └── script.js      # JavaScript utilities
└── templates/
    ├── base.html      # Navigation template
    ├── login.html     # Login page
    ├── register.html  # Sign-up page
    ├── dashboard.html # Main dashboard
    ├── achievements.html  # Achievements page
    └── leaderboard.html   # Leaderboard page
```

---

## Key Technologies

- **Backend**: Flask + SQLAlchemy ORM
- **Database**: SQLite (auto-created)
- **Frontend**: HTML, CSS, JavaScript
- **Charts**: Chart.js
- **Auth**: Flask-Login + Password hashing

---

## Challenge Categories

1. 🎨 **Creative** - Draw, write, design, photograph
2. 📚 **Learning** - Read articles, learn facts, code practice
3. 👥 **Social** - Help others, call friends
4. 💪 **Sports** - Exercise, walk, stay hydrated

---

## Gamification System

- **Points**: Earn points per completed challenge
- **Levels**: Auto-level up every 100 points
- **Streaks**: Track daily completion streaks
- **Badges**: Earn special badges for milestones
  - Dedicated (10 completions)
  - On Fire (7-day streak)
  - Rising Star (Level 5)

---

## Troubleshooting

**Problem**: "Module not found" error
- **Solution**: `pip install -r requirements.txt`

**Problem**: Port already in use
- **Solution**: Change port in app.py, last line: `app.run(debug=True, port=5001)`

**Problem**: Database issues
- **Solution**: Delete `dailyquest.db` and restart app

---

## Future Enhancements

- Email notifications
- Push notifications
- AI challenge suggestions
- Social sharing
- Mobile app
- Custom challenges

---

**Ready to start your quest? Run `python app.py` and begin! ⚔️**
