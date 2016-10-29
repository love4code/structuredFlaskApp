from . import auth
from .. import db
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, \
    current_user
from ..models import User
from ..email import send_email
from .forms import LoginForm, RegistrationForm, ChangePasswordForm


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
# before request hook only applies to the current blueprint


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account',
               'auth/email/confirm', user=current_user, token=token)
    flash('A new Confirmation Link has benn sent to your email account.')
    return redirect(url_for('main.index'))

@auth.before_app_request
def before_request():
    # A user is logged in (current_user.is_authenticated() must return True)
    # The account for the user is not confirmed.
    # The requested endpoint (accessible as request.endpoint) is outside of
    # the authentication blueprint and is not for a static file.
    # Access to the authentication routes needs to be granted,
    # as those are the routes that will enable the user to confirm the
    # account or perform other account management functions.

    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.endpoint[:5] != 'auth.'\
            and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


# Change User Password


@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate():
        # If data is present
        if current_user.verify_password(form.old_password.data):
            # set password to new password
            current_user.password = form.password.data
            # update db session
            db.session.add(current_user)
            flash('Your password has been updated.')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid password.')
            # Redirect back to change password form
    return render_template("auth/change_password.html", form=form)
