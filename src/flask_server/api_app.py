"""Marshall HTTP requests to transport-agnostic controllers.

All transport-specific code please put here.

"""
import inspect
from typing import Any, Callable, Dict, List, Optional, ParamSpec, Tuple, TypeVar

from flask import Blueprint, Flask, Response, request
from flask_swagger_ui import get_swaggerui_blueprint

import settings
from controllers.models import APPNoTokenError, HttpCode
from controllers.users.auth import get_token
from controllers.users.create import create_user
from controllers.users.delete import delete_user
from controllers.users.get import get_user
from controllers.users.list import users_list
from controllers.users.update import update_user
from controllers.version import get_version
from journaling import log
from jwt_token import JWT_MIN_LENGTH, token

API_ROOT_URL = ""  # if we need to shift our api from root to deeper path


app = Flask(__name__)
blueprint = Blueprint("blueprint", __name__, url_prefix="/")


@app.after_request  # type: ignore
def after_request(response: Response) -> Response:
    """After-request flask hook to add CORS headers according to settings."""
    assert settings.config
    if settings.config.web_enableCrossOriginRequests:
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS, DELETE, PUT"
        response.headers[
            "Access-Control-Allow-Headers"
        ] = "DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range,Authorization"
        response.headers["Access-Control-Expose-Headers"] = "Content-Length,Content-Range"
    return response


@app.route(f"{API_ROOT_URL}/<path:path>", methods=["OPTIONS"])  # type: ignore
@app.route(f"{API_ROOT_URL}/", methods=["OPTIONS"])  # type: ignore
def options_handler() -> Response:
    """Handle only unspecified below paths.

    Others handles by application logic and CORS headers added in after-request flask hook
    So I this this is unecessary part but I am too lazy to check..
    """
    assert settings.config
    log.debug(f"Options were requested for {request.full_path}")
    response = Response()
    response.headers["Content-Type"] = "text/plain; charset=utf-8"
    response.status_code = 204
    if settings.config.web_enableCrossOriginRequests:
        response.headers["Access-Control-Max-Age"] = 1728000  # type: ignore
    return response


def auth_token() -> Optional[Dict[str, Any]]:
    """Get auth token from headers and pass it to handler."""
    if not (auth_header := request.headers.get("Authorization")):
        return None
    if len(auth_header.split()) < 2:
        # Try to use it without 'Bearer' prefix - such as from Swagger UI tools
        if len(auth_header) < JWT_MIN_LENGTH:
            raise APPNoTokenError(
                f'Expected in Authorization HTTP header: "Bearer <token>", but got\n{auth_header}'
            )
    else:
        auth_header = auth_header.split()[1]
    return token.decode(auth_header)


Param = ParamSpec("Param")
RetType = TypeVar("RetType")


def api(  # type: ignore
    handler: Callable[Param, RetType],
    bparams: Optional[List[str]] = None,
    raw: Optional[bool] = False,
):
    """Prepare handler to be used as API endpoint.

    If bparams, then add body parameters into the handler parameters, if body parameters names are
    specified in `body` (if no such parameters in request body then returns whole body as
    the first and the only parameter)

    Add all query params into the handler parameters.

    Add auth_user with auth() if such a parameter exists in handler.

    Jsonify result.
    If this is not success then expected error message as a result and wraps it into {'status': messsage}
    """

    def api_wrapper(*args, **kwargs):  # type: ignore  # pylint: disable=too-many-branches
        """Wrapp for API handlers."""
        try:
            if bparams:
                body_obj = request.get_json()
                for param in bparams:
                    if isinstance(body_obj, dict) and param in body_obj:
                        val = body_obj[param]
                    else:
                        if len(bparams) == 1:
                            val = body_obj
                        else:
                            log.debug(
                                f"No parameter {param} in request:\n{request.data!r} ({body_obj})"
                            )
                            return (
                                f"No parameter {param} in request:\n{request.data!r}",
                                HttpCode.wrong_request,
                            )
                    kwargs[param] = val
            if request.args:
                for param in request.args:
                    kwargs[param] = request.args[param]

            # should be last so nothing could inject decoded token
            log.debug(f"API wraps handler with args: {inspect.getfullargspec(handler).args}")
            # if 'auth_user' in inspect.getfullargspec(handler).args:
            # If the handler expects authenticated user (has 'auth_user' param), we pass token to it.
            # Controller's wrapper (@auth_user) will convert token into auth_user param for the handler.
            #
            # Here is transport layer so we just pass decoded token data to controller's logic.
            kwargs["auth_token"] = auth_token()

            result = handler(*args, **kwargs)

        except APPNoTokenError as e:
            log.debug(f"Wrong token format: {e}", exc_info=True)
            result = {"status": str(e)}, HttpCode.no_token  # type: ignore
        except Exception as e:
            log.debug(f"Transport exception: {e}", exc_info=True)
            result = {"status": str(e)}, HttpCode.wrong_request  # type: ignore
        else:
            if raw:  # Only if success, if exception we return API error
                return result
        if isinstance(result, tuple):
            code = result[1]
            result = result[0]
        else:
            code = HttpCode.success
        if code not in HttpCode.successes and isinstance(result, str):
            result = {"status": result}  # type: ignore
        return result, code

    return api_wrapper


app.add_url_rule(
    f"{API_ROOT_URL}/auth",
    "get_token",
    api(get_token, bparams=["email", "password"]),
    methods=["POST"],
)
app.add_url_rule(
    f"{API_ROOT_URL}/users/<string:user_id>", "delete_user", api(delete_user), methods=["DELETE"]
)
app.add_url_rule(
    f"{API_ROOT_URL}/users",
    "create_user",
    api(create_user, bparams=["new_user"]),
    methods=["POST"],
)
app.add_url_rule(
    f"{API_ROOT_URL}/users/<string:user_id>",
    "update_user",
    api(update_user, bparams=["update_user"]),
    methods=["PUT"],
)
app.add_url_rule(f"{API_ROOT_URL}/users", "users_list", api(users_list), methods=["GET"])
app.add_url_rule(
    f"{API_ROOT_URL}/users/<string:user_id>", "get_user", api(get_user), methods=["GET"]
)
app.add_url_rule(f"{API_ROOT_URL}/version", "get_version", get_version, methods=["GET"])

app.register_blueprint(blueprint)


# Route for serving the OpenAPI specification file
@app.route("/swagger.yaml")  # type: ignore
def serve_openapi_spec() -> Tuple[str, int, Dict[str, Any]]:
    """Generate Swagger UI base on Swagger spec."""
    with open("openapi_server/openapi/openapi.yaml", "r", encoding="utf8") as file:
        content = file.read()
    return content, 200, {"Content-Type": "text/yaml"}


SWAGGER_URL = "/ui"  # URL for exposing Swagger UI (without trailing '/')
API_URL = "http://127.0.0.1:5000/swagger.yaml"

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={"app_name": "Test application"},  # Swagger UI config overrides
    # oauth_config={  # OAuth config. See https://github.com/swagger-api/swagger-ui#oauth2-configuration .
    #    'clientId': "your-client-id",
    #    'clientSecret': "your-client-secret-if-required",
    #    'realm': "your-realms",
    #    'appName': "your-app-name",
    #    'scopeSeparator': " ",
    #    'additionalQueryStringParams': {'test': "hello"}
    # }
)

app.register_blueprint(swaggerui_blueprint)
