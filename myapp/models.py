#models 
from myapp import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
#allows to set up isAuthenticate etc 
from flask_login import UserMixin
from datetime import datetime

#login management 
# allows us to use this in templates for isUser stuff 
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    jobs = db.relationship('AppliedJob', backref='author', lazy=True)


    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

#going to use this in our login view 
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f"Username {self.username}"

class AppliedJob(db.Model):
    __tablename__ = 'applied_jobs'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(140), nullable=False)
    company = db.Column(db.String(140), nullable=False)
    date_applied = db.Column(db.String(140), nullable=False)
    accepted = db.Column(db.Boolean, default=False, nullable=False)
    in_process = db.Column(db.Boolean, default=False, nullable=False)
    rejected = db.Column(db.Boolean, default=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


    def __init__(self, title, company, date_applied, accepted, in_process,rejected, user_id):
        self.title = title
        self.company = company
        self.date_applied = date_applied
        self.accepted = accepted
        self.in_process = in_process
        self.rejected = rejected
        self.user_id = user_id
    
    def __repr__(self):
        return f"Job ID: {self.id} -- Date: {self.date} --- Title: {self.Title}"