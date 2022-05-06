from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required, login_user, logout_user
from myblog.forms import LoginForm
from myblog.models import User
from myblog.utils import redirect_back

bp_auth = Blueprint('auth', __name__)


@bp_auth.route('/login', methods=['GET', 'POST'])
def login(next=None):
    if current_user.is_authenticated:
        return redirect(url_for('blog.index'))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user is not None and user.validate_password(password):
            login_user(user, remember=True)
            return redirect_back()
        else:
            flash('Invalid username or password')
    return render_template('auth/login.html', form=form)


@bp_auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('blog.index'))
