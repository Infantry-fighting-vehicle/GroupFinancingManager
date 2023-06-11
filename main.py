from flask import *
from api import *

app = Flask(__name__)
# app.register_blueprint(account_api, url_prefix='/user')
# app.register_blueprint(group_api, url_prefix='/group')

app.add_url_rule("/user", methods=["GET", "POST"], view_func=accountList)
app.add_url_rule("/user/login", methods=["POST"], view_func=login)
app.add_url_rule("/user/logout", view_func=logout)
app.add_url_rule("/user/<username>", methods=["GET", "PUT", "DELETE"], view_func=getUserBytUsername)

app.add_url_rule('/group', methods=['POST'], view_func=create_function)
app.add_url_rule('/group/list', methods=['GET'], view_func=list_avaliable_groups)
app.add_url_rule('/group/<group_id>', methods=['GET', 'PUT', 'DELETE'], view_func=group_management)
#route('/group/<group_id>/send_invitation', methods=['POST'])
app.add_url_rule('/group/join', methods=['POST'], view_func=join_group)
app.add_url_rule('/group/<group_id>/kick', methods=['DELETE'], view_func=kick_users)
app.add_url_rule('/group/<group_id>/purchase', methods=['POST'], view_func=purchase_create)
app.add_url_rule('/group/<group_id>/purchase/<purchase_id>', methods=['DELETE'], view_func=purchase_delete)
# route('/group/purchase/<purchase_id>', methods=['PUT'])
# app.add_url_rule('/group/purchase/<purchase_id>', methods=['GET'], view_func=get_purchase)
#route("/user/", methods=["POST", "GET"])
#route("/user/login")
#route("/user/logout")
#route("/user/<username>", methods=["GET", "PUT", "DELETE"])

# @app.route("/")
# # @app.route("/api/v1/hello-world-16")
# @app.route("/api/v1/hello-world-<var>")
# @app.route("/api")

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