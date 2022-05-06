import logging
import os
import sys
from pathlib import Path

root = Path(__file__).parent
sys.path.insert(0, str(root))
os.chdir(str(root))
logging.getLogger('waitress').setLevel(logging.INFO)

from myblog import app

application = app.wsgi_app

if not root.joinpath('myblog', 'myblog.sqlite').exists():
    from myblog import db, User
    with app.app_context():
        db.create_all()
        admin = User(username='admin')
        admin.set_password('$th4nothing')
        db.session.add(admin)
        will = User(username='will')
        will.set_password('w1LL1314')
        db.session.add(will)
        db.session.commit()
