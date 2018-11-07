import flask_transmute
from flask import Flask, Blueprint
from controllers.user_create import user_create
from controllers.user_delete import user_delete
from controllers.user_list import user_list


app = Flask(__name__)
blueprint = Blueprint("blueprint", __name__, url_prefix="/")

user_delete = flask_transmute.route(app, paths='/users', methods=['DELETE'])(user_delete)
user_create = flask_transmute.route(app, paths='/users', methods=['POST'])(user_create)
#user_update = flask_transmute.route(app, paths='/users/<id>', methods=['PUT'])(user_update)
#user_by_id = flask_transmute.route(app, paths='/users/<id>', methods=['GET'])(user_by_id)
user_list = flask_transmute.route(app, paths='/users', methods=['GET'])(user_list)


app.register_blueprint(blueprint)

flask_transmute.add_swagger(app, "/swagger.json", "/swagger")

app.run()
