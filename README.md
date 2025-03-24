# 📝 Flask Reminder App

A simple Flask-based **note-taking and reminder application** that allows users to **add, delete, and receive reminders via email** for their notes.

## 🚀 Features

✅ **User Authentication** – Register/Login using Flask-Login & Bcrypt  
✅ **Add & Delete Notes** – Users can create and manage their notes  
✅ **Email Reminders** – Automated email notifications when a note is added or deleted  
✅ **Database Storage** – Uses SQLite (or PostgreSQL in production) to store notes  
✅ **Scheduler for Reminders** – APScheduler schedules reminders dynamically  

---

## ⚙️ Installation & Setup

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/flask-reminder-app.git
cd flask-reminder-app

2️⃣ Create a Virtual Environment & Install Dependencies
bash
python -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate     # For Windows
pip install -r requirements.txt

3️⃣ Set Up Environment Variables
touch .env
Inside .env, add:
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your_secret_key
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_email_password

🏃‍♂️ Running the App
bash
flask run

🎯 Database Setup
By default, the app uses SQLite. To create the database:
flask shell
>>> from app import db
>>> db.create_all()
>>> exit()


🛠 Tech Stack
Flask – Web framework

Flask-Login – User authentication

Flask-Mail – Email reminders

Flask-WTF – Form handling

SQLite/PostgreSQL – Database

APScheduler – Scheduled reminders

🎯 Future Improvements
🔹 User-selectable reminder times
🔹 SMS reminders using Twilio
🔹 Mobile-friendly UI (Bootstrap/React frontend)

📧 Contact
📩 Email: 23204001@apsit.edu.in






