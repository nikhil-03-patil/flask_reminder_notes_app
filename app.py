from flask import Flask, flash, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, logout_user, LoginManager, login_required, current_user
from config import Config  # Import Config class directly
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length,ValidationError
from flask_bcrypt import Bcrypt
from flask import flash
from flask_mail import Mail, Message
import smtplib
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime


app = Flask(__name__)

# Load configuration
app.config.from_object(Config)  # Use Config class from config.py
mail = Mail(app)

# Initialize database
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


# this login_manager part allows our app and flasklogin to work together to help user login, load user and logout
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# reloads user id stored in user session
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
# Define User Model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)


# define note model
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))



class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"}
    )

    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder":"Password"})
    email = StringField(validators=[InputRequired(), Length(min=4, max=50)], render_kw={"placeholder": "Email"})
    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()

        if existing_user_username:
            raise ValidationError("The username already exists. Please choose different one!")



class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder":"Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder":"Password"})

    submit = SubmitField("Login")


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
            else:
                return("Invalid password", "danger")

    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password = hashed_password, email = form.email.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))


    return render_template('register.html', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if request.method =='POST':
        content = request.form.get('note')
        msg = Message('New Note added', sender='nikhilrpatil03@gmail.com', recipients=[current_user.email])
        msg.body = f'Hello {current_user.username},\n\nYou just added a new note: "{content}"'
        mail.send(msg)
        if content:
            new_note = Note(content=content, user_id = current_user.id)
            db.session.add(new_note)
            db.session.commit()
    notes = Note.query.filter_by(user_id = current_user.id).all()
        
    return render_template('dashboard.html', notes=notes)

@app.route('/delete_note/<int:note_id>', methods = ['POST'])
@login_required
def delete_note(note_id):
    note = Note.query.get(note_id)
    msg = Message('Note Deleted', sender='nikhilrpatil03@gmail.com', recipients=[current_user.email])
    msg.body = f'Hello {current_user.username},\n\nYou just deleted a note: "{note.content}"'
    mail.send(msg)

    if note.user_id != current_user.id:
        return "Unauthorized", 403
    
    db.session.delete(note)
    db.session.commit()
    flash("Note deleted successfully!", "success")
    return redirect(url_for('dashboard'))


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

def send_reminder():
    with app.app_context():
        users = User.query.all()
        for user in users:
            msg = Message('Daily Reminder' , sender="nikhilrpatil03@gmail.com" , recipients=[user.email])
            msg.body = f' hello {user.username}, \n\nThis is you daily reminder to check your notes!'
            mail.send(msg)
        print(f"Reminder emails send at {datetime.now()}")

# Setup APScheduler
scheduler = BackgroundScheduler()
scheduler.add_job(send_reminder, 'interval', hours=1)  # Runs every 24 hours
scheduler.start()

if __name__ == "__main__":
    app.run(debug=True)
