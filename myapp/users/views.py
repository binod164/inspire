from crypt import methods
from operator import methodcaller
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from itsdangerous import json
from myapp import db
from myapp.models import User
from myapp.users.forms import RegistrationForm, LoginForm, UpdateUserForm
from myapp.models import User, AppliedJob
import requests

users = Blueprint('users', __name__) # dont forget to register this in __init__.py 


# register
@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data, password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Thanks for Registration!')
        return redirect(url_for('users.login'))
    
    return render_template('register.html', form=form)

# login
@users.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()

        if user.check_password(form.password.data) and user is not None:

            login_user(user)
            flash('Log in Success!')

            next = request.args.get('next')

            if next ==None or not next[0]=='/':
                next = url_for('core.index')

            return redirect(next)

    return render_template('login.html',form=form)

# logout
@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('core.info')) #once the user has logged out we will redirect them back home


#account (update UserForm)
@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    req = requests.get("https://zenquotes.io/api/quotes")
    data = json.loads(req.content)

    # response = urllib.request.urlopen(url)
    # quotes = response.read()
    # dict = json.loads(quotes)

    # quotes = []

    # for quote in dict["results"]:
    #     quote = {
    #         "quotes": quote["q"],
    #     }
        
    #     quotes.append(quote)

    # return {"results": quotes}
    return render_template('account.html', data = data)



@users.route('/<username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    applied_jobs = AppliedJob.query.filter_by(author=user).order_by(AppliedJob.date.desc()).paginate(page=page, per_page=5) 
    return render_template('user_applied_jobs.html', applied_jobs=applied_jobs, user=user)