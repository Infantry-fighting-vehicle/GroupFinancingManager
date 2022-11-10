from flask import *
from api import *

app = Flask(__name__)
app.register_blueprint(account_api, url_prefix='/user')
app.register_blueprint(group_api, url_prefix='/group')

@app.after_request
def add_cors_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Headers', 'Cache-Control')
    response.headers.add('Access-Control-Allow-Headers', 'X-Requested-With')
    response.headers.add('Access-Control-Allow-Headers', 'Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE')
    return response

@app.route("/")
def hello_world():
    return "<p>Hello world!<br /><br />Use this link to get to completed task <a href='/api/v1/hello-world-16'>here</a></p>"

# @app.route("/api/v1/hello-world-16")
# def greeting():
#     return f"<p>Hello world 16</p>"


@app.route("/api/v1/hello-world-<var>")
def greeting(var):
    return f"<p>Hello world {var}</p>"

@app.route("/api")
def api():
    return {'something' : 1}