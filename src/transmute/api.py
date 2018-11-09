"""
Transmute version of app
API should be described in code and the app can auto-generate Open API (swagger) UI from the code.
"""
import flask_transmute
from flask import Flask, Blueprint
from transmute.controllers.user_create import user_create
from transmute.controllers.user_delete import user_delete
from transmute.controllers.user_list import user_list
from transmute_core import describe
from functools import partial


app = Flask(__name__)
blueprint = Blueprint("blueprint", __name__, url_prefix="/")
route = partial(flask_transmute.route, app)

user_delete = route(paths='/users', methods=['DELETE'])(
    describe(
        paths='/users', methods=['DELETE'],  # we have to duplicate due to bug https://github.com/toumorokoshi/flask-transmute/issues/11
        query_parameters=['id'],
        parameter_descriptions={'id': 'ID of user to delete'}
    )(user_delete)
)

user_create = route(paths='/users', methods=['POST'])(
    describe(
        paths='/users', methods=['POST'],
        parameter_descriptions={
            'name': 'Name of new user',
            'email': 'Email of new user'
        }
    )(user_create)
)

#user_update = flask_transmute.route(app, paths='/users/<id>', methods=['PUT'])(user_update)
#user_by_id = flask_transmute.route(app, paths='/users/<id>', methods=['GET'])(user_by_id)
user_list = route(paths='/users', methods=['GET'])(
    describe(
        paths='/users', methods=['GET'],
        parameter_descriptions={ # all params are query by default only for GET
            'page': 'Page number, starting from 0. By default 0.',
            'per_page': 'Items on page. By default 10 000.',
            'return': 'A list of pets.',
        }
    )(user_list)
)


app.register_blueprint(blueprint)
flask_transmute.add_swagger(app, "/swagger.json", "/swagger")
