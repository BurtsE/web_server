from flask import Flask, render_template, session, redirect
from requests.requests import request_app
from auth.routes import auth_app
from basket.routes import basket_app
import json

app = Flask(__name__)
app.register_blueprint(request_app, url_prefix='/requests')
app.register_blueprint(auth_app, url_prefix='/auth')
app.register_blueprint(basket_app, url_prefix='/basket')

app.config['DB_CONFIG'] = json.load(open('configs/db.json', 'r'))
app.config['PERMISSION_CONFIG'] = json.load(open('configs/permissions.json', 'r'))
app.config['SECRET_KEY'] = 'super secret key'


@app.route('/')
def index():
    return render_template('base.html')


@app.route('/exit')
def exit():
    session = {}
    return "Окончание работы"

@app.route('/session-clear')
def session_clear():
    session.clear()
    return redirect('/')

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001)  # localhost
