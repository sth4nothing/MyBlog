from loguru import logger

from .app import app
from .ext import bootstrap, db, login_manager
from .models import Comment, Post, PostTag, Tag, User
from .views import bp_auth, bp_blog, bp_tag, bp_user

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
