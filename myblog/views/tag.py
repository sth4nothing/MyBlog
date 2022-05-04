from flask import Blueprint, redirect, render_template, url_for
from loguru import logger
from myblog.ext import db
from myblog.models import Tag

bp_tag = Blueprint('tag', __name__)


@bp_tag.route('/')
def index():
    tags = Tag.query.all()
    return render_template('tag/index.html', tags=tags)


@bp_tag.route('/<int:tag_id>')
def detail(tag_id):
    tag = Tag.query.get(tag_id)
    if not tag:
        return redirect(url_for('tag.index'))
    return render_template('tag/detail.html', tag=tag)


@bp_tag.route('/<int:tag_id>/delete')
def delete(tag_id):
    tag = Tag.query.get(tag_id)
    if not tag:
        return redirect(url_for('tag.index'))
    if tag.posts:
        return redirect(url_for('tag.detail', tag_id=tag_id))
    logger.info(f'{tag.tag_str} deleted')
    db.session.delete(tag)
    db.session.commit()
    return redirect(url_for('tag.index'))
