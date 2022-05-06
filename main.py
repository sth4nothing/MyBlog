import os
import sys
from pathlib import Path

root = Path(__file__).parent
sys.path.insert(0, str(root))
os.chdir(str(root))

from myblog import app

application = app.wsgi_app
