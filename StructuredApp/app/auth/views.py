from . import auth
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required
from .forms import LoginForm
from ..models import User

# Signing In

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for(
                'main.index'))
        flash('Invalid Username or Password')
    return render_template('auth/login.html', form=form)

# Singing Out

@auth.route('/logout')
@login_required
def logout():
    """Log user out and redirect to main.index"""
    logout_user()
    flash('You Have Been logged Out')
    return redirect(url_for('main.index'))


