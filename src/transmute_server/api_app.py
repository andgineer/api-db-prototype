import inspect
from functools import partial
from itertools import chain

import flask_transmute
from flask import Blueprint, Flask
from transmute_core import Response, describe

from controllers import models
from controllers.users.auth import get_token
from controllers.users.create import create_user
from controllers.users.delete import delete_user
from controllers.users.list import users_list
from journaling import log
from jwt_token import token

app = Flask(__name__)
blueprint = Blueprint("blueprint", __name__, url_prefix="/")
route = partial(flask_transmute.route, app)


def api(handler, add_auth=True):
    """Decorate for API handlers."""

    def wrapper(*args, **kwargs):
        if kwargs["Authorization"] is not None:
            token_tokens = kwargs["Authorization"].split(" ")
            token_value = token_tokens[1] if len(token_tokens) > 1 else token_tokens[0]
            kwargs["auth_token"] = token.decode(token_value)
        del kwargs["Authorization"]
        result = handler(*args, **kwargs)
        if result[1] != 200:
            log.debug(f"Error response: {result}")
            return Response(result[0], result[1])
        return result[0]

    # Add Authorization argument to decorated function
    signature = inspect.signature(handler)
    params = []
    for param in signature.parameters.values():
        params.append(param)
    if add_auth:
        params.append(
            inspect.Parameter(
                "Authorization",
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
                default=None,
                annotation=str,
            )
        )
    wrapper.__signature__ = signature.replace(parameters=params)
    wrapper.__name__ = handler.__name__
    return wrapper


error_responces = {
    401: {"type": str, "description": "No or wrong user token in request"},
    500: {"type": str, "description": "Unhandled exception"},
    403: {"type": str, "description": "Unauthorized"},
    501: {"type": str, "description": "Wrong request format etc"},
    400: {
        "type": str,
        "description": "Application level error like user already exists and so on",
    },
}

user_delete = route(paths="/users/{user_id}", methods=["DELETE"])(
    describe(  # we have to duplicate due to bug https://github.com/toumorokoshi/flask-transmute/issues/11
        paths="/users/{user_id}",
        methods=["DELETE"],
        header_parameters=["Authorization"],
        parameter_descriptions={"user_id": "ID of user to delete"},
        response_types=dict(
            chain(error_responces.items(), {200: {"type": str, "description": "Success"}}.items())
        ),
    )(
        api(delete_user)
    )
)

user_create = route(paths="/users", methods=["POST"])(
    describe(
        paths="/users",
        methods=["POST"],
        body_parameters=["new_user"],
        header_parameters=["Authorization"],
        parameter_descriptions={"new_user": "Parameters of user to create"},
        response_types=dict(
            chain(
                error_responces.items(),
                {200: {"type": models.NewUserReply, "description": "Success"}}.items(),
            )
        ),
    )(api(create_user))
)


auth = route(paths="/auth", methods=["POST"])(
    describe(
        paths="/auth",
        methods=["POST"],
        body_parameters=["email", "password"],
        parameter_descriptions={"email": "login"},
        response_types=dict(
            chain(
                error_responces.items(),
                {200: {"type": models.TokenReply, "description": "Success"}}.items(),
            )
        ),
    )(api(get_token))
)

# user_update = flask_transmute.route(app, paths='/users/<id>', methods=['PUT'])(user_update)
# user_by_id = flask_transmute.route(app, paths='/users/<id>', methods=['GET'])(user_by_id)
user_list = route(paths="/users", methods=["GET"])(
    describe(
        paths="/users",
        methods=["GET"],
        header_parameters=["Authorization"],
        parameter_descriptions={  # all params are query by default only for GET
            "page": "Page number, starting from 0. By default 0.",
            "per_page": "Items on page. By default 10 000.",
            "return": "A list of pets.",
            "Authorization": "Security token",
        },
        response_types=dict(
            chain(
                error_responces.items(),
                {200: {"type": models.UsersList, "description": "Success"}}.items(),
            )
        ),
    )(api(users_list))
)


app.register_blueprint(blueprint)
flask_transmute.add_swagger(app, "/swagger.json", "/swagger")
