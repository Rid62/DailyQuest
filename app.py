import sqlite3
import os
import json
from flask import Flask, g, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import google.generativeai as genai
# 1. تحميل الإعدادات
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'super_secret_key_123')
DATABASE = 'DailyQuest.db'

# --- إدارة قاعدة البيانات ---

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# إعداد Gemini
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-1.5-flash')

def generate_daily_quests(user_id, category, level):
    """توليد مهام يومية باستخدام Google Gemini مجاناً"""
    prompt = f"""
    Create exactly 3 daily challenges for a user interested in {category} at a {level} level.
    Return ONLY a JSON object with a key "quests" containing a list of objects with "title" and "description".
    Example format: {{"quests": [{{"title": "Ex", "description": "Ex"}}]}}
    """
    
    try:
        # طلب التوليد من Gemini
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(response_mime_type="application/json")
        )
        
        content = json.loads(response.text)
        quests = content.get('quests', [])
        
        db = get_db()
        for q in quests:
            db.execute('''INSERT INTO challenges (user_id, title, description, category) 
                          VALUES (?, ?, ?, ?)''', 
                       (user_id, q['title'], q['description'], category))
        db.commit()
        
    except Exception as e:
        print(f"Gemini Error: {e}")
        # إذا فشل الذكاء الاصطناعي، نستخدم المهام الافتراضية كما فعلنا سابقاً
        # (كود الـ fallback الذي كتبناه سابقاً)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        category = request.form.get('category')
        level = request.form.get('level')

        if password != confirm_password:
            flash("Passwords do not match!", "danger")
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)
        db = get_db()
        try:
            db.execute('''INSERT INTO users (username, password_hash, main_category, user_level) 
                          VALUES (?, ?, ?, ?)''', 
                       (username, hashed_password, category, level))
            db.commit()
            flash("Account created! Please login.", "success")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("Username already exists!", "danger")
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        db = get_db()
        user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()

        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('Dashboard'))
        else:
            flash("Invalid credentials!", "danger")
            
    return render_template('login.html')

@app.route('/Dashboard')
def Dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    
    # جلب مهام اليوم
    quests = db.execute('SELECT * FROM challenges WHERE user_id = ? AND date_assigned = CURRENT_DATE', 
                        (session['user_id'],)).fetchall()
    
    if not quests:
        generate_daily_quests(user['id'], user['main_category'], user['user_level'])
        quests = db.execute('SELECT * FROM challenges WHERE user_id = ? AND date_assigned = CURRENT_DATE', 
                            (session['user_id'],)).fetchall()
        
    return render_template('Dashboard.html', user=user, quests=quests)

@app.route('/complete_quest/<int:quest_id>', methods=['POST'])
def complete_quest(quest_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    db = get_db()
    db.execute('UPDATE users SET points = points + 10 WHERE id = ?', (session['user_id'],))
    db.execute('DELETE FROM challenges WHERE id = ? AND user_id = ?', (quest_id, session['user_id']))
    db.commit()
    flash("Great job! +10 Points. 🎉", "success")
    return redirect(url_for('Dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/Leaderboard')
def Leaderboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    db = get_db()
    # جلب أفضل 10 مستخدمين حسب النقاط
    top_users = db.execute('''
        SELECT username, points, main_category 
        FROM users 
        ORDER BY points DESC 
        LIMIT 10
    ''').fetchall()
    
    return render_template('Leaderboard.html', users=top_users)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    db = get_db()
    if request.method == 'POST':
        new_category = request.form.get('category')
        new_level = request.form.get('level')
        
        db.execute('UPDATE users SET main_category = ?, user_level = ? WHERE id = ?', 
                   (new_category, new_level, session['user_id']))
        db.commit()
        flash("Profile updated successfully! Tomorrow's quests will match your new goals.")
        return redirect(url_for('Dashboard'))

    user = db.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    return render_template('profile.html', user=user)
    
if __name__ == '__main__':
    app.run(debug=True)