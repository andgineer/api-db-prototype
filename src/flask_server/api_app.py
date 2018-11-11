from flask import Flask, Blueprint, jsonify, request
from controllers.users.create import create_user
from controllers.users.delete import delete_user
from controllers.users.list import users_list


app = Flask(__name__)
blueprint = Blueprint("blueprint", __name__, url_prefix="/")


def api(handler, body: list=None):
    """
    Jsonifies returned by handler object.
    Add body parameters before call handler, if body parameters names are specified in `body`
    (if no such parameters in request body then returns whole body as the first and
    the only parameter)
    """
    def api_wrapper(*args, **kwargs):
        if body:
            body_obj = request.get_json()
            for param in body:
                if isinstance(body_obj, dict) and param in body_obj:
                    val = body_obj[param]
                else:
                    if len(body) == 1:
                        val = body_obj
                    else:
                        return f'No parameter {param} in request:\n{request.data}', 400
                kwargs.update({param: val})
        result = handler(*args, **kwargs)
        if isinstance(result, tuple):
            code = result[1]
            result = result[0]
        else:
            code = 200
        return jsonify(result), code
    return api_wrapper

app.add_url_rule('/users/<string:user_id>', 'delete_user', api(delete_user), methods=['DELETE'])
app.add_url_rule('/users', 'create_user', api(create_user, body=['new_user']), methods=['POST'])
app.add_url_rule('/users', 'users_list', api(users_list), methods=['GET'])


app.register_blueprint(blueprint)
