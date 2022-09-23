from flask import *

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello world!<br /><br />Use this link to get to completed task <a href='/api/v1/hello-world-16'>here</a></p>"

# @app.route("/api/v1/hello-world-16")
# def greeting():
#     return f"<p>Hello world 16</p>"


@app.route("/api/v1/hello-world-<var>")
def greeting(var):
    return f"<p>Hello world {var}</p>"