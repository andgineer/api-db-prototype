import flask_transmute
from flask import Flask, Blueprint
from controllers.users.create import create_user
from controllers.users.delete import delete_user
from controllers.users.list import users_list
from transmute_core import describe
from functools import partial


app = Flask(__name__)
blueprint = Blueprint("blueprint", __name__, url_prefix="/")
route = partial(flask_transmute.route, app)

user_delete = route(paths='/users/{user_id}', methods=['DELETE'])(
    describe(
        paths='/users/{user_id}', methods=['DELETE'],  # we have to duplicate due to bug https://github.com/toumorokoshi/flask-transmute/issues/11
        parameter_descriptions={'user_id': 'ID of user to delete'}
    )(delete_user)
)

user_create = route(paths='/users', methods=['POST'])(
    describe(
        paths='/users', methods=['POST'],
        body_parameters=['new_user'],
        parameter_descriptions={
            'new_user': 'Parameters of user to create'
        }
    )(create_user)
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
    )(users_list)
)


app.register_blueprint(blueprint)
flask_transmute.add_swagger(app, "/swagger.json", "/swagger")
