from quart import Quart, render_template, send_file


app = Quart(__name__)

@app.route('/')
async def index():
    return await render_template('index.html')

@app.route('/favicon.ico')
async def favicon():
    return await send_file('static/favicon.ico')
