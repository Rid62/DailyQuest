# 🎮 DailyQuest: An AI-Powered RPG Productivity Tool
#### Video Demo: [Paste your YouTube URL here]
#### Description: 
A gamified task management system that uses Artificial Intelligence to turn personal development into an engaging adventure.

---

## 🌟 Project Overview
**DailyQuest** is a full-stack web application developed as the final project for Harvard's **CS50x 2026**. The project addresses the universal problem of procrastination and the "boring" nature of traditional to-do lists. 

While most productivity apps rely on the user to manually enter every task, DailyQuest leverages the **Google Gemini AI API** to act as a "Dungeon Master" for real life. Users select an interest (Coding, Fitness, Reading, or Languages) and a difficulty level, and the AI generates three dynamic, personalized "Quests" every 24 hours. By completing these quests, users earn **Experience Points (XP)**, level up, and compete on a global leaderboard.

---

## 🧠 Design Choices and Logic

### 1. Why Flask and Python?
I chose **Flask** because of its flexibility. Unlike larger frameworks like Django, Flask allowed me to understand the "under the hood" mechanics of routing and session management, which was a key learning goal in CS50x. Python’s rich ecosystem made integrating the **Google Generative AI SDK** straightforward and efficient.

### 2. The Power of Generative AI (Gemini 1.5 Flash)
The most critical design choice was moving from static tasks to AI-generated content. I integrated **Gemini 1.5 Flash** because of its high speed and its ability to output structured **JSON**. By using "Prompt Engineering," I forced the AI to return data in a specific format that my SQL database could understand, preventing the app from crashing due to unexpected text responses.

### 3. Database Architecture (SQLite)
I designed a relational database using **SQLite3**. The schema ensures that:
- Users have unique profiles with hashed passwords for security.
- Quests are linked to specific users and dates, preventing users from doing the same task twice.
- XP is calculated and stored in real-time, allowing the Leaderboard to be always up-to-date.

---

## 📂 Detailed File Descriptions

### `app.py`
This is the main controller. It handles:
- **Authentication**: Using `Werkzeug` to hash passwords and manage user sessions.
- **AI Logic**: The `generate_daily_quests` function which constructs the prompt and communicates with Google Gemini.
- **Game Logic**: Functions that handle XP rewards and ensure users can only complete a quest once.

### `DailyQuest.db`
The SQLite database file. It contains the following tables:
- `users`: Stores `id`, `username`, `hash`, `main_category`, `user_level`, and `total_xp`.
- `challenges`: Stores the AI-generated quests, including `title`, `description`, `category`, and a `completed` status.

### `templates/` (The View Layer)
- `layout.html`: The base template using Jinja2 blocks. It includes the Bootstrap 5 CDN and a responsive Navbar.
- `index.html`: The landing page designed to attract new users with a clean "Hero" section.
- `Dashboard.html`: The core of the app where users interact with their daily quests.
- `Leaderboard.html`: Displays the top 10 players based on XP.
- `profile.html`: Allows users to change their settings, which directly influences the AI's future quest generation.
* `login.html`: A clean, user-friendly form that allows returning users to access their accounts. It includes validation feedback to ensure a smooth user experience.
    * `register.html`: The entry point for new users. It collects essential data such as username, interest category, and difficulty level, which are then used to personalize the AI-generated quests.
### `static/`
- `style.css`: Contains custom CSS to give the app a modern, "gaming" aesthetic that Bootstrap alone couldn't provide, such as rounded pill buttons and custom card shadows.
static/javascript/:

script.js: A client-side script that enhances the registration process by providing real-time visual feedback. It checks if the "Password" and "Confirm Password" fields match, changing the border color to green for success or red for a mismatch.
### `.env` & `requirements.txt`
- `.env`: Holds the `GEMINI_API_KEY` and `FLASK_SECRET_KEY` to keep sensitive data safe.
- `requirements.txt`: Lists all dependencies (`Flask`, `google-generativeai`, `python-dotenv`) to make the project reproducible.

---

## 🤖 AI and Academic Honesty
In compliance with **CS50x Academic Honesty** rules:
- **AI as a Feature**: Google Gemini is a functional part of the software.
- **AI as a Helper**: I used AI tools (Gemini/ChatGPT) to help debug specific Flask errors and to improve the visual CSS of the dashboard. However, the core logic, database design, and architecture were entirely created by me.

---

## 🏁 Installation and Setup
To run this project locally:
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`.
3. Create a `.env` file and add your `GEMINI_API_KEY`.
4. Run the app: `python -m flask run`.

---

## 🎯 Conclusion
DailyQuest is more than just a website; it’s a demonstration of how modern AI can be integrated into classic web architectures to create something useful and fun. This project helped me master SQL relationships, API integration, and the importance of user experience design.