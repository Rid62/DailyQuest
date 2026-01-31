#!/usr/bin/env python
"""Initialize database with fresh schema"""

from app import app, db, Challenge

with app.app_context():
    print("Dropping all tables...")
    db.drop_all()
    
    print("Creating new tables...")
    db.create_all()
    
    print("Adding sample challenges...")
    challenges = [
        Challenge(title='Sketch something', description='Draw whatever comes to mind', category='creative', points=10),
        Challenge(title='Write a short story', description='Write 100+ words about anything', category='creative', points=15),
        Challenge(title='Take a creative photo', description='Capture something beautiful', category='creative', points=10),
        Challenge(title='Design a cool poster', description='Create digital or physical art', category='creative', points=15),
        Challenge(title='Read an article', description='Read a 5-10 min article on any topic', category='learning', points=10),
        Challenge(title='Learn a new word', description='Learn and use a new word today', category='learning', points=5),
        Challenge(title='Try a coding snippet', description='Write and run 10 lines of code', category='learning', points=15),
        Challenge(title='Watch an educational video', description='Watch a 10-15 min learning video', category='learning', points=10),
        Challenge(title='Call a friend', description='Have a genuine conversation', category='social', points=10),
        Challenge(title='Help someone', description='Do something nice for someone else', category='social', points=15),
        Challenge(title='Leave a compliment', description='Genuinely compliment 3 people', category='social', points=10),
        Challenge(title='Join a community', description='Attend or join a group activity', category='social', points=15),
        Challenge(title='10-minute workout', description='Do any exercise for 10 minutes', category='sports', points=10),
        Challenge(title='Go for a walk', description='Walk for 20+ minutes', category='sports', points=10),
        Challenge(title='Drink 8 glasses of water', description='Stay hydrated all day', category='sports', points=5),
        Challenge(title='Stretch for 5 minutes', description='Do stretching exercises', category='sports', points=5),
    ]
    
    for challenge in challenges:
        db.session.add(challenge)
    
    db.session.commit()
    print(f"✓ Database initialized with {Challenge.query.count()} challenges")
