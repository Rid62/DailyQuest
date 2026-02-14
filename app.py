import sqlite3
import os
import json
from flask import Flask, g, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from openai import OpenAI

# 1. تحميل الإعدادات من ملف .env
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'super_secret_key_123')
DATABASE = 'DailyQuest.db'

# 2. إعداد عميل OpenAI
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

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

# --- وظائف الذكاء الاصطناعي ---

def generate_daily_quests(user_id, category, level):
    """توليد 3 مهام يومية باستخدام OpenAI وحفظها في قاعدة البيانات"""
    prompt = f"""
    Create exactly 3 daily challenges for a user interested in {category} at a {level} level.
    The challenges should be actionable, small, and encouraging.
    Return ONLY a JSON object with a key "quests" containing a list of objects with "title" and "description".
    Example format: {{"quests": [{"title": "Ex", "description": "Ex"}]}}
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": "You are a helpful life coach."},
                      {"role": "user", "content": prompt}],
            response_format={ "type": "json_object" }
        )

        content = json.loads(response.choices[0].message.content)
        quests = content.get('quests', [])
        
        db = get_db()
        for q in quests:
            db.execute('''INSERT INTO challenges (user_id, title, description, category, date_assigned) 
                          VALUES (?, ?, ?, ?, CURRENT_DATE)''', 
                       (user_id, q['title'], q['description'], category))
        db.commit()
    except Exception as e:
        print(f"Error calling OpenAI: {e}")
        flash("We couldn't generate new quests right now, showing default ones.")

# --- المسارات (Routes) ---

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
            # تأكد أن السطر داخل دالة generate_daily_quests يبدو هكذا بالضبط:
            db.execute('''INSERT INTO challenges (user_id, title, description, category) 
                        VALUES (?, ?, ?, ?)''', 
           (user_id, q['title'], q['description'], category))
            db.commit()
            flash("Registration successful! Please login.", "success")
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
    
    if user is None:
        return redirect(url_for('login'))
    
    # جلب مهام اليوم للمستخدم
    quests = db.execute('SELECT * FROM challenges WHERE user_id = ? AND date_assigned = CURRENT_DATE', 
                        (session['user_id'],)).fetchall()
    
    # إذا لم توجد مهام اليوم، نطلب من AI توليدها
    if not quests:
        generate_daily_quests(user['id'], user['main_category'], user['user_level'])
        quests = db.execute('SELECT * FROM challenges WHERE user_id = ? AND date_assigned = CURRENT_DATE', 
                            (session['user_id'],)).fetchall()
        
    return render_template('Dashboard.html', user=user, quests=quests)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/complete_quest/<int:quest_id>', methods=['POST'])

def generate_daily_quests(user_id, category, level):
    """توليد 3 مهام يومية باستخدام OpenAI وحفظها في قاعدة البيانات"""
    
    # لاحظ أننا استخدمنا {{ }} للأقواس التي تخص JSON و { } للمتغيرات فقط
    prompt = f"""
    Create exactly 3 daily challenges for a user interested in {category} at a {level} level.
    The challenges should be actionable, small, and encouraging.
    Return ONLY a JSON object with a key "quests" containing a list of objects with "title" and "description".
    Example format: {{"quests": [{{"title": "Ex", "description": "Ex"}}]}}
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful life coach."},
                {"role": "user", "content": prompt}
            ],
            response_format={ "type": "json_object" }
        )

        content = json.loads(response.choices[0].message.content)
        quests = content.get('quests', [])
        
        db = get_db()
        for q in quests:
            db.execute('''INSERT INTO challenges (user_id, title, description, category) 
                          VALUES (?, ?, ?, ?)''', 
                       (user_id, q['title'], q['description'], category))
        db.commit()
    except Exception as e:
        print(f"Error calling OpenAI: {e}")
        flash("We couldn't generate new quests right now.")
if __name__ == '__main__':
    app.run(debug=True)