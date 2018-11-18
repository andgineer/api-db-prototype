"""
Marshalling HTTP requests to transport-agnostic controllers.

All transport-specific code please put here.

"""
from flask import Flask, Blueprint, jsonify, request
from controllers.users.create import create_user
from controllers.users.delete import delete_user
from controllers.users.list import users_list
from controllers.users.get import get_user
from controllers.users.auth import get_token
from controllers.models import SUCCESS_CODES, SUCCESS_CODE, API_ERROR_CODE
from journaling import log
from jwt_token import token
import inspect


app = Flask(__name__)
blueprint = Blueprint("blueprint", __name__, url_prefix="/")


def auth_token():
    """
    Gets auth token from headers and pass it to handler
    """
    auth_header = request.headers.get('Authorization')
    if auth_header:
        return token.decode(auth_header.split(" ")[1])
    else:
        return None


def api(handler, bparams: list=None):
    """
    If bparams, then add body parameters into the handler parameters, if body parameters names are
    specified in `body` (if no such parameters in request body then returns whole body as
    the first and the only parameter)

    Add all query params into the handler parameters.

    Add auth_user with auth() if such a parameter exists in handler.

    Jsonify result.
    If this is not success then expected error message as a result and wraps it into {'status': messsage}
    """
    def api_wrapper(*args, **kwargs):
        if bparams:
            body_obj = request.get_json()
            for param in bparams:
                if isinstance(body_obj, dict) and param in body_obj:
                    val = body_obj[param]
                else:
                    if len(bparams) == 1:
                        val = body_obj
                    else:
                        log.debug(f'No parameter {param} in request:\n{request.data} ({body_obj})')
                        return f'No parameter {param} in request:\n{request.data}', API_ERROR_CODE
                kwargs.update({param: val})
        if request.args:
            for param in request.args:
                kwargs.update({param: request.args[param]})

        # should be last so nothing could inject decoded token
        if 'auth_user' in inspect.getfullargspec(handler).args:
            """
            If the handler expects authenticated user (has 'auth_user' param), we pass token to it. 
            Controller's wrapper (@auth_user) will convert token into auth_user param for the handler.
            
            Here is transport layer so we just pass decoded token data to controller's logic.
            """
            kwargs.update({'auth_token': auth_token()})

        result = handler(*args, **kwargs)
        if isinstance(result, tuple):
            code = result[1]
            result = result[0]
        else:
            code = SUCCESS_CODE
        if code not in SUCCESS_CODES and isinstance(result, str):
            result = {'status': result}
        return jsonify(result), code
    return api_wrapper


app.add_url_rule('/auth', 'get_token', api(get_token, bparams=['email', 'password']), methods=['POST'])
app.add_url_rule('/users/<string:user_id>', 'delete_user', api(delete_user), methods=['DELETE'])
app.add_url_rule('/users', 'create_user', api(create_user, bparams=['new_user']), methods=['POST'])
app.add_url_rule('/users', 'users_list', api(users_list), methods=['GET'])
app.add_url_rule('/users/<string:user_id>', 'get_user', api(get_user), methods=['GET'])


app.register_blueprint(blueprint)
