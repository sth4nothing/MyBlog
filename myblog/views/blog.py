import datetime
import math

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user
from loguru import logger
from myblog.ext import db
from myblog.forms import CommentForm
from myblog.models import Comment, Post, Tag

bp_blog = Blueprint('blog', __name__)


@bp_blog.route('/')
def index(page=1, size=20):
    if size < 5:
        return redirect(url_for('blog.index', size=5))
    page_num = math.ceil(Post.query.count() / size)
    if page_num == 0:
        return render_template('blog/index.html', page=1, page_num=1, posts=[])
    if page < 1 or page > page_num:
        return redirect(url_for('blog.index', page=1, size=size))
    posts = Post.query.order_by(Post.modification_time.desc()).paginate(
        page, size)
    return render_template('blog/index.html',
                           posts=posts.items,
                           page=page,
                           page_num=page_num)


@bp_blog.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get(post_id)
    if post:
        if current_user.is_anonymous:
            return render_template('blog/post.html', post=post)
        form = CommentForm()
        if form.validate_on_submit():
            try:
                comment = Comment(content=form.content.data,
                                  post_id=post_id,
                                  user_id=current_user.user_id,
                                  creation_time=datetime.datetime.now())
                db.session.add(comment)
                db.session.commit()
                return redirect(url_for('blog.post', post_id=post_id))
            except Exception as e:
                db.session.rollback()
                logger.error(e)
                flash(str(e))
        return render_template('blog/post.html', post=post, form=form)
    return redirect(url_for('blog.index'))
