"""
Controllers from swagger code-gen modified by hand.
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
from openapi_server.models.update_user import UpdateUser
from openapi_server.models.user import User  # pylint: disable=unused-import
from openapi_server.models.user_credentials import UserCredentials

# todo use swagger auth not hack with header extraction


def extract_token(authorization: str) -> Dict[str, Any]:
    """Return dict to create controllers.auth.AuthUser."""
    # get in from Authorization header like "Bearer <token>" or just "<token>"
    authorization = authorization if len(authorization.split()) < 2 else authorization.split()[1]
    # decode JWT payload where we pass email and group, check JWT validity
    return token.decode(authorization)  # type: ignore


def get_token(user_credentials: UserCredentials = None) -> Dict[str, Any]:
    """
    Get access token for the user

    Validate user credentials with DB and return JWT token for the user.
    """
    if connexion.request.is_json:
        user_credentials = UserCredentials.from_dict(connexion.request.get_json())
    return controllers.users.auth.get_token(user_credentials.email, user_credentials.password)  # type: ignore


def create_user(body: Dict[str, Any]) -> ApiResult:
    """
    Create a user

    Return {"id": <user_id>} or (<error message>, <HTTP code>).
    """
    authorization = connexion.request.headers["Authorization"]
    new_user = body.get("new_user", body)

    return controllers.users.create.create_user(
        auth_token=extract_token(authorization), new_user=new_user
    )


def get_user(user_id: str) -> ApiResult:
    """Get info for a specific user."""
    authorization = connexion.request.headers["Authorization"]
    return controllers.users.get.get_user(auth_token=extract_token(authorization), user_id=user_id)


def list_users(
    per_page: int = PER_PAGE_DEFAULT, page: int = PAGE_DEFAULT
) -> ApiResult:  # noqa: E501
    """List all users

    :param page: Page number of results to return.
    :type page: str
    :param per_page: Number of items on page.
    :type per_page: str

    :rtype: Users
    """
    authorization = connexion.request.headers["Authorization"]
    return controllers.users.list.users_list(
        auth_token=extract_token(authorization), page=page, per_page=per_page
    )


def update_user(
    user_id: str, update_user: UpdateUser
) -> ApiResult:  # pylint: disable=unused-argument
    """Update details of particular user.

    :param user_id: The id of the user to update
    :type user_id: str
    :param update_user:
    :type update_user: dict | bytes

    :rtype: Empty
    """
    authorization = connexion.request.headers["Authorization"]
    if connexion.request.is_json:
        update_user = UpdateUser.from_dict(connexion.request.get_json())  # noqa: E501
    return controllers.users.update.update_user(
        auth_token=extract_token(authorization), update_user_obj=update_user
    )


def delete_user(userId: str) -> ApiResult:  # noqa: E501
    """Delete the user.

    :param userId: The id of the user to delete
    :type userId: str
    """
    authorization = connexion.request.headers["Authorization"]
    return controllers.users.delete.delete_user(
        auth_token=extract_token(authorization), user_id=userId
    )
