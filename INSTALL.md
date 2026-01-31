# 🎯 DailyQuest - Complete Installation & Usage Guide

## ✅ What Has Been Built

Your **DailyQuest** application is **100% complete** and ready to run. It includes:

### Backend (Python/Flask)
- ✅ User authentication system (register/login/logout)
- ✅ SQLite database with 5 interconnected tables
- ✅ Challenge management system
- ✅ Points and level progression
- ✅ Streak tracking
- ✅ Badge/achievement system
- ✅ Leaderboard functionality
- ✅ REST API endpoints
- ✅ User statistics and analytics

### Frontend (HTML/CSS/JavaScript)
- ✅ Responsive design (mobile/tablet/desktop)
- ✅ Modern purple gradient theme
- ✅ Authentication pages (login/register)
- ✅ Interactive dashboard
- ✅ Chart.js visualizations
- ✅ Achievement showcase
- ✅ Leaderboard display
- ✅ Smooth animations and transitions

### Database
- ✅ SQLite with pre-loaded sample challenges
- ✅ User management
- ✅ Challenge tracking
- ✅ Badge system
- ✅ User preferences

---

## 🚀 Installation & Running

### Option 1: Windows (Easiest)
Simply run the batch file:
```bash
run.bat
```
This will:
1. Create virtual environment
2. Install dependencies
3. Start the application
4. Open instructions

### Option 2: macOS/Linux
Run the shell script:
```bash
chmod +x run.sh
./run.sh
```

### Option 3: Manual Installation

1. **Navigate to project folder**:
   ```bash
   cd FINAL_PROJECT
   ```

2. **Create virtual environment** (optional but recommended):
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
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

5. **Open in browser**:
   ```
   http://localhost:5000
   ```

---

## 📋 First Time Setup (In App)

1. **Register Account**
   - Click "Sign up here" link on login page
   - Create username, email, password
   - Submit form

2. **Login**
   - Enter credentials
   - Click Login

3. **Complete Your First Challenge**
   - See "Today's Challenge" on dashboard
   - Read the challenge description
   - Click "Mark as Complete"
   - See points awarded!

4. **Explore Features**
   - View dashboard stats
   - Check achievements page
   - View leaderboard

---

## 🎮 Features Overview

### Dashboard
- **Today's Challenge**: Daily quest from 4 categories
- **Stats**: Level, Points, Streak, Total Quests
- **Progress Charts**: 30-day history & category breakdown
- **Badges**: View earned achievements

### Challenge Categories
- 🎨 **Creative**: Drawing, writing, photography, design
- 📚 **Learning**: Articles, facts, coding
- 👥 **Social**: Helping others, friend calls
- 💪 **Sports**: Exercise, walks, hydration

### Gamification
- **Points**: Earn 5-15 per challenge
- **Levels**: Auto-level every 100 points
- **Streaks**: Daily completion tracking
- **Badges**: Automatic achievement unlocking
  - Dedicated (10 completions)
  - On Fire (7-day streak)
  - Rising Star (Level 5)

### Leaderboard
- Top 50 users by points
- Your rank display
- Competitive element

---

## 📁 Project Files Explained

### Main Files
| File | Purpose |
|------|---------|
| `app.py` | Main Flask application + all logic |
| `requirements.txt` | Python dependencies |
| `run.bat` | Windows startup script |
| `run.sh` | macOS/Linux startup script |

### Templates (HTML Pages)
| File | Purpose |
|------|---------|
| `base.html` | Navigation bar template |
| `login.html` | Login page |
| `register.html` | Registration page |
| `dashboard.html` | Main dashboard with charts |
| `achievements.html` | Achievement showcase |
| `leaderboard.html` | Competitive ranking |

### Static Assets
| File | Purpose |
|------|---------|
| `style.css` | All styling (600+ lines) |
| `script.js` | JavaScript utilities |

### Documentation
| File | Purpose |
|------|---------|
| `README.md` | Full documentation |
| `QUICKSTART.md` | Quick start guide |
| `PROJECT_SUMMARY.md` | Project overview |
| `INSTALL.md` | This file |

---

## 🔧 Customization

### Change Database Secret Key (Important!)
In `app.py`, line 10:
```python
app.config['SECRET_KEY'] = 'change-this-to-something-random'
```

### Add More Challenges
In `app.py`, find `init_db()` function (around line 390):
```python
Challenge(
    title='Your challenge',
    description='What to do',
    category='creative',  # creative, learning, social, sports
    points=10
)
```

### Adjust Point Values
Modify the `points=` parameter in Challenge creation.

### Create Custom Badges
Edit `check_and_award_badges()` function (around line 340).

### Change Port
In `app.py`, last line:
```python
app.run(debug=True, port=5001)  # Use port 5001 instead
```

### Disable Debug Mode (Production)
Change last line to:
```python
app.run(debug=False)
```

---

## 🐛 Troubleshooting

### Error: "Module not found" (e.g., flask, sqlalchemy)
**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

### Error: "Port 5000 already in use"
**Solution**: Change port in app.py last line or stop other process
```python
app.run(debug=True, port=5001)
```

### Error: "Database locked"
**Solution**: Delete `dailyquest.db` and restart
```bash
rm dailyquest.db  # macOS/Linux
del dailyquest.db  # Windows
python app.py
```

### Error: Python not found
**Solution**: Install Python from https://www.python.org
- Make sure to check "Add Python to PATH"

### App won't start
**Solution**: Check for error messages and ensure:
- Python 3.8+ is installed
- All dependencies are installed (`pip install -r requirements.txt`)
- Port 5000 is available
- You're in the FINAL_PROJECT directory

---

## 📊 Database Schema

### Users Table
- username, email, password_hash
- points, level, streak
- last_activity, created_at

### Challenges Table
- title, description, category
- difficulty, points
- created_at

### ChallengeCompletion Table
- user_id, challenge_id
- completed_at, shared

### Badges Table
- user_id, name, description
- icon, earned_at

### UserPreference Table
- user_id, preferred_category
- notifications_enabled

---

## 🎯 Usage Examples

### After Login, You Can:

1. **View Daily Challenge**
   - It's displayed on dashboard
   - Only one per day

2. **Complete Challenge**
   - Click "Mark as Complete"
   - Get points instantly
   - See stats update

3. **Track Progress**
   - View level and points
   - See 30-day chart
   - Check category breakdown

4. **View Achievements**
   - See earned badges
   - Check progress toward new badges
   - Share on social media (future feature)

5. **Check Leaderboard**
   - See top 50 users
   - Find your rank
   - Compare scores

---

## 🔒 Security Notes

- Passwords are hashed with Werkzeug
- SQL injection protected with SQLAlchemy ORM
- Session management with Flask-Login
- CSRF tokens available in forms

**For production**, change:
1. SECRET_KEY (random string)
2. DEBUG=False
3. Use HTTPS
4. Use PostgreSQL instead of SQLite

---

## 📱 Features by Page

### Login/Register Pages
- Form validation
- Error messages
- Password security
- Account creation

### Dashboard
- Daily challenge display
- Interactive completion button
- Real-time stats
- Progress charts
- Badge showcase

### Achievements
- Badge showcase
- Statistics overview
- Future badges list
- Completion tracking

### Leaderboard
- Top 50 ranking
- Your position
- Points comparison
- Medal indicators (🥇🥈🥉)

---

## 🌐 Responsive Design

The app works perfectly on:
- ✅ Desktop (1920x1080+)
- ✅ Tablet (768x1024)
- ✅ Mobile (320x568+)
- ✅ All modern browsers

---

## 📈 Future Enhancements

Ready to build upon this? Consider adding:
1. Email notifications for daily challenges
2. Push notifications
3. User profiles and following
4. Comments on achievements
5. Friend leaderboards
6. AI-powered challenge suggestions
7. Mobile native app
8. Challenge difficulty selection
9. Reward shop (redeem points)
10. Social media integration

---

## ✨ Tips & Tricks

1. **Build a Streak**: Complete a challenge every day
2. **Level Up**: Accumulate 100 points per level
3. **Earn Badges**: Hit specific milestones
4. **Climb Leaderboard**: Focus on higher-point challenges
5. **Mix Categories**: Try all 4 challenge types

---

## 🎓 Learning Resources

This project teaches you:
- Flask web development
- SQLAlchemy ORM
- User authentication
- Database design
- Responsive CSS
- JavaScript interactivity
- REST API design
- HTML templating
- Git version control

---

## 📞 Support

If you encounter issues:
1. Check error messages in terminal
2. Review the code comments in app.py
3. Check browser console (F12) for JavaScript errors
4. Ensure all dependencies are installed
5. Try deleting database and restarting

---

## 🎉 You're All Set!

Your DailyQuest application is complete and ready to use.

**To start**:
```bash
python app.py
```

Then open: **http://localhost:5000**

---

## 📄 License & Credits

Open source project - feel free to modify, extend, and share!

Built with:
- Flask
- SQLAlchemy
- Chart.js
- Bootstrap-inspired design

---

**Happy Questing! May your streaks be legendary! ⚔️⭐**

*Last Updated: January 31, 2026*
