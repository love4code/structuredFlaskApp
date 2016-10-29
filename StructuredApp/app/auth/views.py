from . import auth
from .. import db
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, \
    current_user
from ..models import User
from ..email import send_email
from .forms import LoginForm, RegistrationForm


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

# Define User Registration Route

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """Register a new user in our database"""

    form = RegistrationForm()
    if form.validate():
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=form.password.data)
        db.session.add(user)
        # we need user id to generate a token so we are doing a db commit
        #  now
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm your Account',
                   'auth/email/confirm', user=user, token=token)
        flash('A Confirmation email has benn sent to your email account')

        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account.')
    else:
        flash('The confirmation link is invalid or has expired.')
        return redirect(url_for('main.index'))


