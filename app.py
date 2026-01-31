from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import random
import os
import json
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dailyquest.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Configure OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

# ==================== DATABASE MODELS ====================

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    points = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)
    streak = db.Column(db.Integer, default=0)
    streak_freezes = db.Column(db.Integer, default=0)
    last_activity = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Profile fields (onboarding)
    age = db.Column(db.Integer)
    job_status = db.Column(db.String(100))
    goals = db.Column(db.Text)
    struggles = db.Column(db.Text)
    onboarded = db.Column(db.Boolean, default=False)
    
    # Relationships
    completions = db.relationship('ChallengeCompletion', backref='user', lazy=True, cascade='all, delete-orphan')
    badges = db.relationship('Badge', backref='user', lazy=True, cascade='all, delete-orphan')
    preferences = db.relationship('UserPreference', backref='user', lazy=True, cascade='all, delete-orphan')
    analysis = db.relationship('AIAnalysis', backref='user', lazy=True, cascade='all, delete-orphan', uselist=False)
    daily_greetings = db.relationship('DailyGreeting', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def add_points(self, amount):
        self.points += amount
        if self.points >= self.level * 100:
            self.level += 1
        self.last_activity = datetime.utcnow()
        db.session.commit()

class AIAnalysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    analysis_summary = db.Column(db.Text)
    welcome_letter = db.Column(db.Text)
    suggested_vibe = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class DailyGreeting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    greeting_text = db.Column(db.Text)
    ai_quests = db.relationship('AIQuest', backref='greeting', lazy=True, cascade='all, delete-orphan')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    date = db.Column(db.Date)

class AIQuest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    greeting_id = db.Column(db.Integer, db.ForeignKey('daily_greeting.id'), nullable=False)
    quest_id = db.Column(db.Integer)
    category = db.Column(db.String(50))
    title = db.Column(db.String(200))
    description = db.Column(db.Text)
    points = db.Column(db.Integer, default=10)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Challenge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)  # creative, learning, social, sports
    difficulty = db.Column(db.String(20), default='medium')  # easy, medium, hard
    points = db.Column(db.Integer, default=10)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    completions = db.relationship('ChallengeCompletion', backref='challenge', lazy=True, cascade='all, delete-orphan')

class ChallengeCompletion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenge.id'), nullable=False)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)
    shared = db.Column(db.Boolean, default=False)
    proof = db.Column(db.Text)  # User's proof of completion (anti-cheating mechanism)
    
    # Composite unique constraint - user can only complete each challenge once per day
    __table_args__ = (db.UniqueConstraint('user_id', 'challenge_id', 'completed_at', name='unique_daily_completion'),)

class Badge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    icon = db.Column(db.String(50))
    earned_at = db.Column(db.DateTime, default=datetime.utcnow)

class UserPreference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    preferred_category = db.Column(db.String(50))
    notifications_enabled = db.Column(db.Boolean, default=True)

# ==================== AUTHENTICATION ROUTES ====================

@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(int(user_id))
    except Exception as e:
        # Handle database schema mismatches - return None to force re-login
        print(f"Error loading user: {e}")
        return None

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            return render_template('register.html', error='Username already exists'), 400
        
        if User.query.filter_by(email=email).first():
            return render_template('register.html', error='Email already exists'), 400
        
        user = User(username=username, email=email)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        return redirect(url_for('dashboard'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid username or password'), 401
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# ==================== MAIN ROUTES ====================

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    today = datetime.utcnow().date()
    
    # Get today's challenge completion
    today_completion = ChallengeCompletion.query.filter_by(user_id=current_user.id).filter(
        db.func.date(ChallengeCompletion.completed_at) == today
    ).first()
    
    # Get today's challenges (multiple)
    today_challenges = get_daily_challenges(current_user.id, count=5)
    today_challenge = get_daily_challenge(current_user.id)
    
    # Get user stats
    all_completions = ChallengeCompletion.query.filter_by(user_id=current_user.id).all()
    badges = Badge.query.filter_by(user_id=current_user.id).all()
    
    return render_template('dashboard.html', 
                         challenge=today_challenge,
                         challenges=today_challenges,
                         completed_today=today_completion is not None,
                         user=current_user,
                         total_completions=len(all_completions),
                         badges=badges)

@app.route('/api/daily-challenge')
@login_required
def api_daily_challenge():
    challenge = get_daily_challenge(current_user.id)
    if challenge:
        return jsonify({
            'id': challenge.id,
            'title': challenge.title,
            'description': challenge.description,
            'category': challenge.category,
            'points': challenge.points
        })
    return jsonify({'error': 'No challenge available'}), 404

@app.route('/api/complete-challenge/<int:challenge_id>', methods=['POST'])
@login_required
def complete_challenge(challenge_id):
    challenge = Challenge.query.get(challenge_id)
    if not challenge:
        return jsonify({'error': 'Challenge not found'}), 404
    
    today = datetime.utcnow().date()
    existing = ChallengeCompletion.query.filter_by(
        user_id=current_user.id,
        challenge_id=challenge_id
    ).filter(db.func.date(ChallengeCompletion.completed_at) == today).first()
    
    if existing:
        return jsonify({'error': 'Already completed today'}), 400
    
    # Get proof from request
    data = request.get_json() or {}
    proof = data.get('proof', '').strip()
    
    # Validate proof (minimum 50 characters)
    if not proof or len(proof) < 50:
        return jsonify({'error': 'Proof must be at least 50 characters'}), 400
    
    completion = ChallengeCompletion(
        user_id=current_user.id, 
        challenge_id=challenge_id,
        proof=proof  # Store the proof
    )
    db.session.add(completion)
    
    # Check level before points
    old_level = current_user.level
    
    # Award points
    current_user.add_points(challenge.points)
    
    # Check for streak
    update_user_streak(current_user.id)
    
    # Check for badges
    check_and_award_badges(current_user.id)
    
    db.session.commit()
    
    # Check if leveled up
    leveled_up = current_user.level > old_level
    
    return jsonify({
        'success': True,
        'points': challenge.points,
        'user_points': current_user.points,
        'level': current_user.level,
        'streak': current_user.streak,
        'leveled_up': leveled_up,
        'new_level': current_user.level if leveled_up else old_level
    })

@app.route('/achievements')
@login_required
def achievements():
    badges = Badge.query.filter_by(user_id=current_user.id).all()
    completions = ChallengeCompletion.query.filter_by(user_id=current_user.id).all()
    
    return render_template('achievements.html',
                         badges=badges,
                         total_completions=len(completions),
                         user=current_user)

@app.route('/leaderboard')
@login_required
def leaderboard():
    users = User.query.order_by(User.points.desc()).limit(50).all()
    user_rank = 1
    for i, u in enumerate(users):
        if u.id == current_user.id:
            user_rank = i + 1
            break
    
    return render_template('leaderboard.html', users=users, user_rank=user_rank, current_user=current_user)

@app.route('/shop')
@login_required
def shop():
    return render_template('shop.html', user=current_user)

@app.route('/api/buy-item', methods=['POST'])
@login_required
def buy_item():
    data = request.get_json()
    item_type = data.get('item')
    cost = data.get('cost')
    
    if current_user.points < cost:
        return jsonify({'error': 'Not enough points'}), 400
    
    if item_type == 'freeze':
        if cost != 100:  # Validate cost
            return jsonify({'error': 'Invalid price'}), 400
        
        current_user.points -= cost
        current_user.streak_freezes += 1
        db.session.commit()
        
        return jsonify({
            'success': True,
            'new_points': current_user.points,
            'new_freezes': current_user.streak_freezes
        })
    
    return jsonify({'error': 'Unknown item'}), 400

@app.route('/api/user-stats')
@login_required
def api_user_stats():
    completions = ChallengeCompletion.query.filter_by(user_id=current_user.id).all()
    
    # Get points by category
    stats_by_category = {}
    for completion in completions:
        cat = completion.challenge.category
        stats_by_category[cat] = stats_by_category.get(cat, 0) + completion.challenge.points
    
    # Get daily completion count for last 30 days
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    recent_completions = ChallengeCompletion.query.filter_by(user_id=current_user.id).filter(
        ChallengeCompletion.completed_at >= thirty_days_ago
    ).all()
    
    daily_stats = {}
    for completion in recent_completions:
        day = completion.completed_at.strftime('%Y-%m-%d')
        daily_stats[day] = daily_stats.get(day, 0) + 1
    
    return jsonify({
        'points': current_user.points,
        'level': current_user.level,
        'streak': current_user.streak,
        'total_completions': len(completions),
        'by_category': stats_by_category,
        'daily': daily_stats
    })

# ==================== HELPER FUNCTIONS ====================

def get_daily_challenge(user_id):
    """Get or create today's challenge for user"""
    today = datetime.utcnow().date()
    
    # Check if user already has a challenge assigned today
    recent_completion = ChallengeCompletion.query.filter_by(user_id=user_id).order_by(
        ChallengeCompletion.completed_at.desc()
    ).first()
    
    if recent_completion and recent_completion.completed_at.date() == today:
        return recent_completion.challenge
    
    # Get user preference
    pref = UserPreference.query.filter_by(user_id=user_id).first()
    
    if pref and pref.preferred_category:
        challenge = Challenge.query.filter_by(category=pref.preferred_category).order_by(
            db.func.random()
        ).first()
    else:
        challenge = Challenge.query.order_by(db.func.random()).first()
    
    return challenge

def get_daily_challenges(user_id, count=5):
    """Get multiple daily challenges for user (for dashboard)"""
    # Get all challenges and randomize them
    challenges = Challenge.query.order_by(db.func.random()).limit(count).all()
    return challenges if challenges else []

def update_user_streak(user_id):
    """Update user's completion streak - with Streak Freeze support"""
    user = User.query.get(user_id)
    today = datetime.utcnow().date()
    yesterday = today - timedelta(days=1)
    
    today_completion = ChallengeCompletion.query.filter_by(user_id=user_id).filter(
        db.func.date(ChallengeCompletion.completed_at) == today
    ).first()
    
    yesterday_completion = ChallengeCompletion.query.filter_by(user_id=user_id).filter(
        db.func.date(ChallengeCompletion.completed_at) == yesterday
    ).first()
    
    # Check day before yesterday (for streak freeze logic)
    day_before_yesterday = today - timedelta(days=2)
    day_before_completion = ChallengeCompletion.query.filter_by(user_id=user_id).filter(
        db.func.date(ChallengeCompletion.completed_at) == day_before_yesterday
    ).first()
    
    if today_completion and yesterday_completion:
        # Consecutive days with activity
        user.streak += 1
    elif today_completion and not yesterday_completion:
        # Missed yesterday, but have a freeze available
        if day_before_completion and user.streak_freezes > 0:
            # Use a freeze - maintain the streak
            user.streak_freezes -= 1
            user.streak += 1
        else:
            # No freeze or no activity before yesterday - reset streak
            user.streak = 1

def check_and_award_badges(user_id):
    """Check and award badges based on user progress"""
    user = User.query.get(user_id)
    completions = ChallengeCompletion.query.filter_by(user_id=user_id).all()
    
    # Badge: 10 Completions
    if len(completions) == 10:
        if not Badge.query.filter_by(user_id=user_id, name='Dedicated').first():
            badge = Badge(user_id=user_id, name='Dedicated', 
                         description='Complete 10 challenges', icon='🏆')
            db.session.add(badge)
    
    # Badge: 7-day streak
    if user.streak >= 7:
        if not Badge.query.filter_by(user_id=user_id, name='On Fire').first():
            badge = Badge(user_id=user_id, name='On Fire',
                         description='7-day completion streak', icon='🔥')
            db.session.add(badge)
    
    # Badge: Level 5
    if user.level >= 5:
        if not Badge.query.filter_by(user_id=user_id, name='Rising Star').first():
            badge = Badge(user_id=user_id, name='Rising Star',
                         description='Reached Level 5', icon='⭐')
            db.session.add(badge)

# ==================== CREATE DATABASE ====================

def init_db():
    """Initialize database with sample data"""
    with app.app_context():
        db.create_all()
        
        # Check if challenges already exist
        if Challenge.query.first():
            return
        
        # Sample challenges
        challenges = [
            # Creative
            Challenge(title='Sketch something', description='Draw whatever comes to mind', 
                     category='creative', points=10),
            Challenge(title='Write a short story', description='Write 100+ words about anything', 
                     category='creative', points=15),
            Challenge(title='Take a creative photo', description='Capture something beautiful', 
                     category='creative', points=10),
            Challenge(title='Design a cool poster', description='Create digital or physical art', 
                     category='creative', points=15),
            
            # Learning
            Challenge(title='Read an article', description='Read a 5-10 min article on any topic', 
                     category='learning', points=10),
            Challenge(title='Learn a new word', description='Learn and use a new word today', 
                     category='learning', points=5),
            Challenge(title='Try a coding snippet', description='Write and run 10 lines of code', 
                     category='learning', points=15),
            Challenge(title='Watch an educational video', description='Watch a 10-15 min learning video', 
                     category='learning', points=10),
            
            # Social
            Challenge(title='Call a friend', description='Have a genuine conversation', 
                     category='social', points=10),
            Challenge(title='Help someone', description='Do something nice for someone else', 
                     category='social', points=15),
            Challenge(title='Leave a compliment', description='Genuinely compliment 3 people', 
                     category='social', points=10),
            Challenge(title='Join a community', description='Attend or join a group activity', 
                     category='social', points=15),
            
            # Sports/Health
            Challenge(title='10-minute workout', description='Do any exercise for 10 minutes', 
                     category='sports', points=10),
            Challenge(title='Go for a walk', description='Walk for 20+ minutes', 
                     category='sports', points=10),
            Challenge(title='Drink 8 glasses of water', description='Stay hydrated all day', 
                     category='sports', points=5),
            Challenge(title='Stretch for 5 minutes', description='Do stretching exercises', 
                     category='sports', points=5),
        ]
        
        for challenge in challenges:
            db.session.add(challenge)
        
        db.session.commit()

# ==================== AI INTEGRATION ====================

def generate_ai_onboarding(user):
    """Generate personalized onboarding analysis using OpenAI"""
    try:
        prompt = f"""Act as a highly empathetic life coach and a close supportive friend. I will provide you with a user's profile: [Age: {user.age}, Occupation: {user.job_status}, Goals: {user.goals}, Main Struggles: {user.struggles}].

Your task:

Analyze their current life stage and personality.

Write a 2-paragraph 'Welcome Letter' as a best friend. Make it feel personal, understanding, and non-judgmental.

Determine the 'Vibe' of the relationship (e.g., 'The Tough-Love Coach' or 'The Gentle Supporter').

Return the response in a structured JSON format with keys: analysis_summary, welcome_letter, and suggested_vibe."""

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a supportive AI assistant that returns JSON responses."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        
        response_text = response.choices[0].message.content
        ai_response = json.loads(response_text)
        
        return ai_response
    except Exception as e:
        print(f"Error generating onboarding: {e}")
        return None

def generate_daily_quests(user):
    """Generate 5 daily quests using OpenAI with proof requirements to prevent cheating"""
    try:
        user_profile = f"Age: {user.age}, Job: {user.job_status}, Goals: {user.goals}"
        
        prompt = f"""You are the 'DailyQuest' AI Best Friend. Based on the user's profile ({user_profile}) and their progress so far, generate 5 unique daily challenges for today.

The 5 Categories required:

Creative: (e.g., sketching, writing, or solving a problem differently).

Learning: (e.g., reading a specific concept related to their goal).

Social: (e.g., a small act of kindness or a specific conversation).

Health/Physical: (e.g., a micro-workout or a mindfulness habit).

Anti-Routine: (e.g., doing a common task in a new way to break stagnation).

Constraints:

The challenges must be realistic for a {user.age} year old who is {user.job_status}.

Include a 'Daily Greeting' that mentions their specific goal ({user.goals}) to show you remember them.

IMPORTANT - Anti-Cheating Requirement:
For each challenge, include a 'proof_type' field that specifies what proof the user must provide:
- If category is 'Learning' or 'Creative': proof_type should be 'summary' (user must write 50+ characters explaining what they learned/created)
- If category is 'Health/Physical': proof_type should be 'description' (user describes the workout, e.g., "30 min run" + duration)
- If category is 'Social': proof_type should be 'reflection' (user reflects on how it felt)
- If category is 'Anti-Routine': proof_type should be 'explanation' (user explains the new way they did it)

Format the output strictly as JSON: {{"morning_greeting": "...", "quests": [{{"id": 1, "category": "Creative", "title": "...", "description": "...", "points": 15, "proof_type": "summary"}}, {{"id": 2, "category": "Learning", "title": "...", "description": "...", "points": 15, "proof_type": "summary"}}, {{"id": 3, "category": "Social", "title": "...", "description": "...", "points": 15, "proof_type": "reflection"}}, {{"id": 4, "category": "Health/Physical", "title": "...", "description": "...", "points": 15, "proof_type": "description"}}, {{"id": 5, "category": "Anti-Routine", "title": "...", "description": "...", "points": 15, "proof_type": "explanation"}}]}}"""

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a supportive AI coach that generates personalized daily quests. Return only valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8
        )
        
        response_text = response.choices[0].message.content
        ai_response = json.loads(response_text)
        
        return ai_response
    except Exception as e:
        print(f"Error generating daily quests: {e}")
        return None

# ==================== NEW ONBOARDING ROUTES ====================

@app.route('/onboarding', methods=['GET', 'POST'])
@login_required
def onboarding():
    if request.method == 'POST':
        # Save user profile
        current_user.age = request.form.get('age', type=int)
        current_user.job_status = request.form.get('job_status')
        current_user.goals = request.form.get('goals')
        current_user.struggles = request.form.get('struggles')
        
        db.session.commit()
        
        # Generate AI analysis
        ai_response = generate_ai_onboarding(current_user)
        
        if ai_response:
            # Save analysis
            analysis = AIAnalysis(
                user_id=current_user.id,
                analysis_summary=ai_response.get('analysis_summary'),
                welcome_letter=ai_response.get('welcome_letter'),
                suggested_vibe=ai_response.get('suggested_vibe')
            )
            db.session.add(analysis)
            current_user.onboarded = True
            db.session.commit()
            
            # Generate first daily quests
            generate_daily_quests_for_user(current_user.id)
            
            return redirect(url_for('dashboard'))
        else:
            return render_template('onboarding.html', error='Could not generate AI analysis. Please try again.')
    
    return render_template('onboarding.html')

@app.route('/analysis')
@login_required
def view_analysis():
    analysis = AIAnalysis.query.filter_by(user_id=current_user.id).first()
    return render_template('analysis.html', analysis=analysis, user=current_user)

@app.route('/api/generate-daily-quests', methods=['POST'])
@login_required
def api_generate_daily_quests():
    """Manually trigger daily quest generation"""
    result = generate_daily_quests_for_user(current_user.id)
    if result:
        return jsonify({'success': True, 'message': 'Daily quests generated!'})
    return jsonify({'success': False, 'error': 'Failed to generate quests'}), 500

def generate_daily_quests_for_user(user_id):
    """Helper function to generate and save daily quests"""
    user = User.query.get(user_id)
    today = datetime.utcnow().date()
    
    # Check if quests already exist for today
    existing = DailyGreeting.query.filter_by(user_id=user_id, date=today).first()
    if existing:
        return existing
    
    ai_response = generate_daily_quests(user)
    
    if ai_response:
        # Create daily greeting
        greeting = DailyGreeting(
            user_id=user_id,
            greeting_text=ai_response.get('morning_greeting'),
            date=today
        )
        db.session.add(greeting)
        db.session.flush()  # Get the ID
        
        # Create AI quests
        for quest in ai_response.get('quests', []):
            ai_quest = AIQuest(
                greeting_id=greeting.id,
                quest_id=quest.get('id'),
                category=quest.get('category'),
                title=quest.get('title'),
                description=quest.get('description'),
                points=quest.get('points', 15)
            )
            db.session.add(ai_quest)
        
        db.session.commit()
        return greeting
    
    return None

@app.route('/api/complete-ai-quest/<int:quest_id>', methods=['POST'])
@login_required
def complete_ai_quest(quest_id):
    """Mark an AI-generated quest as complete"""
    quest = AIQuest.query.get(quest_id)
    
    if not quest:
        return jsonify({'error': 'Quest not found'}), 404
    
    if quest.greeting.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    quest.completed = True
    current_user.add_points(quest.points)
    update_user_streak(current_user.id)
    check_and_award_badges(current_user.id)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'points': quest.points,
        'user_points': current_user.points,
        'level': current_user.level
    })

@app.route('/daily-quests')
@login_required
def daily_quests():
    today = datetime.utcnow().date()
    greeting = DailyGreeting.query.filter_by(user_id=current_user.id, date=today).first()
    
    if not greeting:
        greeting = generate_daily_quests_for_user(current_user.id)
    
    return render_template('daily_quests.html', greeting=greeting, user=current_user)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

