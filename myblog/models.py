import datetime
from functools import cached_property

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from .ext import db


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    posts = db.relationship('Post', back_populates='user', lazy=True)
    comments = db.relationship('Comment', back_populates='user', lazy=True)

    @property
    def is_admin(self):
        return self.username == 'admin'

    def get_id(self):
        return str(self.user_id)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password, password)


class Tag(db.Model):
    __tablename__ = 'tag'
    tag_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tag_str = db.Column(db.String(20), unique=True, nullable=False)
    posts = db.relationship('Post',
                            back_populates='tags',
                            secondary='post_tag',
                            lazy=True)

    def __repr__(self) -> str:
        return f'<Tag "{self.tag_str}">'

    @staticmethod
    def find_or_create(tag_str):
        tag = Tag.query.filter_by(tag_str=tag_str).first()
        if tag is None:
            tag = Tag(tag_str=tag_str)
            db.session.add(tag)
        return tag


class Comment(db.Model):
    __tablename__ = 'comment'
    comment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(500), nullable=False)
    creation_time = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('user.user_id'),
                        nullable=False)
    user = db.relationship('User', back_populates='comments')
    post_id = db.Column(db.Integer,
                        db.ForeignKey('post.post_id'),
                        nullable=False)
    post = db.relationship('Post', back_populates='comments')


class Post(db.Model):
    __tablename__ = 'post'
    post_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('user.user_id'),
                        nullable=False)
    user = db.relationship('User', back_populates='posts')
    creation_time = db.Column(db.DateTime, nullable=False)
    modification_time = db.Column(db.DateTime, nullable=False)
    comments = db.relationship('Comment', back_populates='post', lazy=True)
    tags = db.relationship('Tag', back_populates='posts', secondary='post_tag')

    @property
    def tags_str(self):
        return ', '.join([tag.tag_str for tag in self.tags])

    @cached_property
    def sorted_comments(self):
        return sorted(self.comments,
                      key=lambda x: x.creation_time,
                      reverse=True)

    @staticmethod
    def create(title, content, user):
        t = datetime.datetime.now()
        post = Post(title=title,
                    content=content,
                    user=user,
                    creation_time=t,
                    modification_time=t)
        db.session.add(post)
        return post


class PostTag(db.Model):
    __tablename__ = 'post_tag'
    post_id = db.Column(db.Integer,
                        db.ForeignKey('post.post_id'),
                        primary_key=True)
    tag_id = db.Column(db.Integer,
                       db.ForeignKey('tag.tag_id'),
                       primary_key=True)
