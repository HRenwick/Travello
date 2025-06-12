from flask import Blueprint, render_template, redirect, url_for, flash
from .forms import LoginForm, RegisterForm
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user
from. import db

# Create Blueprint
authbp = Blueprint('auth', __name__ )

# Register Route: Sign up
@authbp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        user_type = form.user_type.data
        # Match User Against Database
        existing_user = db.session.scalar(db.select(User).where(
            (User.username == username) | (User.email == email)))
        if existing_user:
            if existing_user.username == username:
                flash('Username already exists. Please try another.')
            else:
                flash('Email address already exists. Please try another.')
            return redirect(url_for('auth.register'))
        # Protect Password
        pwd_hash = generate_password_hash(password)
        # Instantiate New User
        new_user = User(username=username, email=email, 
                        password_hash=pwd_hash, user_type=user_type)
        db.session.add(new_user)
        db.session.commit()
        flash(f"Welcome aboard, {username}! You're all signed up.")
        print(f"New {user_type} user created: '{username}'")
        return redirect(url_for('auth.login'))
    return render_template('user.html', form=form, heading='Register')

# Register Route: Log In
@authbp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        # Match Username Against Database
        existing_user = db.session.scalar(db.select(User).where(User.username==username))
        if existing_user is None:
            flash('Incorrect username. Please try again.')
        # Check Passwords Match
        elif not check_password_hash(existing_user.password_hash, password):
            flash('Incorrect password. Please try again.')
        else:
            login_user(existing_user)
            flash(f"Pleased to see you again, {username}!")
            print(f"System logged in user: '{username}'")
            return redirect(url_for('main.index'))
    return render_template('user.html', form=form, heading='Log In')

# Register Route: Log Out
@authbp.route('/logout')
def logout():
    username = current_user.username
    logout_user()
    flash('You have successfully logged out of your account.')
    print(f"System logged out user: '{username}'")
    return redirect(url_for('main.index'))