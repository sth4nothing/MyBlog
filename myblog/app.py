import datetime

from flask import Flask, render_template, send_file

from myblog.utils import text_decode

app = Flask(__name__)


@app.template_filter('strftime')
def _jinja2_filter_datetime(dt: datetime.datetime, fmt=None):
    if fmt is None:
        fmt = '%Y-%m-%d %H:%M:%S'
    return dt.strftime(fmt)


@app.template_filter('text_decode')
def _jinja2_filter_text_decode(text):
    return text_decode(text)


@app.route('/favicon.ico')
def favicon():
    return send_file('static/images/favicon.ico')


# @app.route('/')
# def index():
#     return render_template('index.html')
