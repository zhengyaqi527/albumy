from flask import Blueprint, redirect, url_for, render_template, flash
from flask_login import current_user, login_required

from albumy.extensions import db
from albumy.models import User
from albumy.forms.auth import RegisterForm
from albumy.utils import validate_token, generate_token
from albumy.settings import Operations
from albumy.emails import send_confirm_email, send_reset_password_email

auth_bp = Blueprint('auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data.lower()
        username = form.username.data
        password = form.password.data
        user = User(
            name=name,
            email=email,
            username=username,
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Confirm email sent, check your inbox.', 'info')
        return redirect(url_for('.login'))

    return render_template('auth/register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    pass


@auth_bp.route('/logout')
@login_required
def logout():
    pass


@auth_bp.route('/confirm/<token>')
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))

    if validate_token(user=current_user, token=token, operation=Operations.CONFIRM):
        flash('Account confimed.', 'success')
        return redirect(url_for('main.index'))
    else:
        flash('Invalid or expired token.', 'danger')
        return redirect(url_for('.resend_confirmation'))
    

@auth_bp.route('/resend-confirm-email')
def resend_confirm_email():
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    token = generate_token(user=current_user, operation=Operations.CONFIRM)
    send_confirm_email(user=current_user, toktn=token)
    flash('New email has sent, check your inbox.', 'info')

    return redirect(url_for('main.index'))


@auth_bp.route('/forget-password', methods=['GET', 'POST'])
def forget_password():
    pass


@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
@login_required
def reset_password(token):
    pass
