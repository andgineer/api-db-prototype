"""Controllers from swagger code-gen modified by hand.

They proxy to our application logic handlers in controllers folder.
"""
from typing import Any, Dict

import connexion

import controllers.models
import controllers.users.auth
import controllers.users.create
import controllers.users.delete
import controllers.users.get
import controllers.users.list
import controllers.users.update
from controllers.models import PAGE_DEFAULT, PER_PAGE_DEFAULT, ApiResult
from jwt_token import token
from openapi_server.models.user_credentials import UserCredentials

# todo use swagger auth not hack with header extraction


def extract_token(authorization: str) -> Dict[str, Any]:
    """Return dict to create controllers.auth.AuthUser."""
    # get in from Authorization header like "Bearer <token>" or just "<token>"
    authorization = authorization if len(authorization.split()) < 2 else authorization.split()[1]
    # decode JWT payload where we pass email and group, check JWT validity
    return token.decode(authorization)  # type: ignore


def get_token(user_credentials: UserCredentials = None) -> Dict[str, Any]:
    """Get access token for the user.

    Validate user credentials with DB and return JWT token for the user.
    """
    if connexion.request.is_json:
        user_credentials = UserCredentials.from_dict(connexion.request.get_json())
    return controllers.users.auth.get_token(user_credentials.email, user_credentials.password)  # type: ignore


def create_user(body: Dict[str, Any]) -> ApiResult:
    """Create a user.

    Return {"id": <user_id>} or (<error message>, <HTTP code>).
    """
    authorization = connexion.request.headers["Authorization"]
    new_user = body.get("new_user", body)

    return controllers.users.create.create_user(  # type: ignore  # pylint: disable=no-value-for-parameter
        auth_token=extract_token(authorization), new_user=new_user
    )


def get_user(userId: str) -> ApiResult:
    """Get info for a specific user."""
    authorization = connexion.request.headers["Authorization"]
    return controllers.users.get.get_user(  # type: ignore  # pylint: disable=no-value-for-parameter
        auth_token=extract_token(authorization), user_id=userId
    )


def list_users(
    per_page: int = PER_PAGE_DEFAULT, page: int = PAGE_DEFAULT
) -> ApiResult:  # noqa: E501
    """List all users.

    :param page: Page number of results to return.
    :type page: str
    :param per_page: Number of items on page.
    :type per_page: str

    :rtype: Users
    """
    authorization = connexion.request.headers["Authorization"]
    return controllers.users.list.users_list(  # type: ignore  # pylint: disable=no-value-for-parameter
        auth_token=extract_token(authorization), page=page, per_page=per_page
    )


def update_user(userId: str, body: Dict[str, Any]) -> ApiResult:
    """Update details of particular user."""
    authorization = connexion.request.headers["Authorization"]
    update_user_dict = body.get("update_user", body)
    return controllers.users.update.update_user(  # type: ignore  # pylint: disable=no-value-for-parameter
        auth_token=extract_token(authorization), user_id=userId, update_user=update_user_dict
    )


def delete_user(userId: str) -> ApiResult:  # noqa: E501
    """Delete the user.

    :param userId: The id of the user to delete
    :type userId: str
    """
    authorization = connexion.request.headers["Authorization"]
    return controllers.users.delete.delete_user(  # type: ignore  # pylint: disable=no-value-for-parameter
        auth_token=extract_token(authorization), user_id=userId
    )
