from pathlib import Path

from loguru import logger

from .app import app
from .ext import bootstrap, db, login_manager
from .models import Comment, Post, PostTag, Tag, User
from .views import bp_auth, bp_blog, bp_tag, bp_user

root = Path(__file__).parent
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myblog.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'sth4nothing'
app.register_blueprint(bp_blog, url_prefix='/')
app.register_blueprint(bp_auth, url_prefix='/auth')
app.register_blueprint(bp_user, url_prefix='/user')
app.register_blueprint(bp_tag, url_prefix='/tag')
bootstrap.init_app(app)
db.init_app(app)
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.before_first_request
def before_first_request():
    if not root.joinpath('myblog.sqlite').exists():
        db.create_all()
        admin = User(username='admin')
        admin.set_password('$th4nothing')
        db.session.add(admin)
        will = User(username='will')
        will.set_password('w1LL1314')
        db.session.add(will)
        ting = User(username='ting')
        ting.set_password('T1ng1234')
        db.session.add(ting)
        db.session.commit()
        logger.info('Create database and admin user')
