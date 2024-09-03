from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import db
from app.models.user import User
from app.forms.auth import LoginForm
from flask_login import login_user, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        print(username)
        print(password)
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            flash('You have logged in successfully.', 'success')
            print("success")
            return redirect(url_for('AHB.success', message="You have logged in."))
        else:
            print("fail")
            flash('Username or password is incorrect.', 'danger')

    return render_template('AUTH/login.html', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('AHB.index'))

