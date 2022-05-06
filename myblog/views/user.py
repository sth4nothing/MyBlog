import datetime
import math
import re

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user
from loguru import logger
from myblog.utils import dump_db
from myblog.ext import db
from myblog.forms import AdminForm, AdminLoginForm, PostForm
from myblog.models import Comment, Post, Tag, User

bp_user = Blueprint('user', __name__)


@bp_user.route('/')
@login_required
def index(page=1, size=20):
    return redirect(
        url_for('user.user_post',
                user_id=current_user.user_id,
                page=page,
                size=size))


@bp_user.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        try:
            post = Post.create(form.title.data, form.content.data,
                               current_user)
            for tag_str in re.split(r',\s*', form.tags_str.data.strip()):
                if not tag_str:
                    continue
                tag = Tag.find_or_create(tag_str)
                post.tags.append(tag)
            db.session.commit()
            logger.info(f'{current_user.username} create post {post.title}')
            return redirect(url_for('blog.post', post_id=post.post_id))
        except Exception as e:
            db.session.rollback()
            logger.error(e)
    return render_template('user/new_post.html', form=form)


@bp_user.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get(post_id)
    if post and post.user_id == current_user.user_id:
        form = PostForm(obj=post)
        if form.validate_on_submit():
            try:
                post.title = form.title.data
                post.content = form.content.data
                post.tags = []
                post.modification_time = datetime.datetime.now()
                for tag_str in re.split(r',\s*', form.tags_str.data.strip()):
                    if not tag_str:
                        continue
                    tag = Tag.find_or_create(tag_str)
                    post.tags.append(tag)
                db.session.commit()
                logger.info(f'{current_user.username} edit post {post.title}')
                return redirect(url_for('blog.post', post_id=post.post_id))
            except Exception as e:
                db.session.rollback()
                logger.error(e)
        return render_template('user/new_post.html', form=form, post=post)
    elif post:
        return redirect(url_for('blog.post', post_id=post.post_id))
    return redirect(url_for('user.index'))


@bp_user.route('/post/<int:post_id>/delete', methods=['GET'])
@login_required
def delete_post(post_id):
    post = Post.query.get(post_id)
    if post and (post.user_id == current_user.user_id
                 or current_user.is_admin):
        try:
            db.session.delete(post)
            db.session.commit()
            logger.info(f'{current_user.username} delete post {post.title}')
        except Exception as e:
            db.session.rollback()
            logger.error(e)
    return redirect(url_for('user.index'))


@bp_user.route('/<int:user_id>')
def user_post(user_id, page=1, size=20):
    if size < 5:
        return redirect(url_for('user.user_post', user_id=user_id, size=5))
    user = User.query.get(user_id)
    if user is None:
        return redirect(url_for('user.index'))
    q = Post.query.filter_by(user_id=user_id)
    page_num = math.ceil(q.count() / size)
    if page_num == 0:
        return render_template('user/user_post.html',
                               user=user,
                               page=1,
                               page_num=1,
                               posts=[])
    posts = q.order_by(Post.modification_time.desc()).paginate(page, size)
    return render_template('user/user_post.html',
                           user=user,
                           page=page,
                           page_num=page_num,
                           posts=posts.items)


@bp_user.route('/comment/<int:comment_id>/delete', methods=['GET'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get(comment_id)
    if comment:
        if comment.user_id == current_user.user_id or current_user.is_admin:
            try:
                db.session.delete(comment)
                db.session.commit()
                logger.info(
                    f'{current_user.username} delete comment {comment.content}'
                )
                return redirect(url_for('blog.post', post_id=comment.post_id))
            except Exception as e:
                db.session.rollback()
                logger.error(e)
                flash(e)
        return redirect(url_for('blog.post', post_id=comment.post_id))
    return redirect(request.referrer)

@bp_user.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated and current_user.is_admin:
        return redirect(url_for('user.admin'))
    form = AdminLoginForm()
    if form.validate_on_submit():
        admin = User.query.filter_by(username='admin').first()
        if admin and admin.validate_password(form.password.data):
            login_user(admin, remember=True)
            return redirect(url_for('user.admin'))
        flash('Invalid password')
    return render_template('auth/login.html', form=form)


@bp_user.route('/admin', methods=['GET', 'POST'])
def admin():
    if not current_user.is_authenticated or not current_user.is_admin:
        return redirect(url_for('user.admin_login'))
    form = AdminForm()
    if form.validate_on_submit():
        if form.export.data:
            data = dump_db()
            if data:
                flash(data)
        elif form.sql.data:
            try:
                ret = list()
                for line in form.sql.data.split(';'):
                    if not line.strip():
                        continue
                    ret.append(db.session.execute(line).all())
                db.session.commit()
                for r in ret:
                    flash(str(r))
            except Exception as e:
                db.session.rollback()
                flash(e)
    return render_template('user/admin.html', form=form)
