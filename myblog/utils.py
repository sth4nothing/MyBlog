import sqlite3
from pathlib import Path
from urllib.parse import urljoin, urlparse

from flask import redirect, request, url_for

project_dir = Path(__file__).resolve().parent


def dump_db():
    db_file = project_dir / 'myblog.sqlite'
    if db_file.exists():
        conn = sqlite3.connect(str(db_file))
        return '\n'.join(line for line in conn.iterdump())
    return ''


def is_safe_url(url):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, url))
    return test_url.scheme in ('http',
                               'https') and ref_url.netloc == test_url.netloc


def redirect_back(default='blog.index', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))