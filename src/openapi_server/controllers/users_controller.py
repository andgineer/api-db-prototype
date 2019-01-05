from openapi_server.models.user import User  # noqa: E501
import controllers.users.create
import controllers.users.delete
import controllers.users.get
import controllers.users.list
import controllers.users.auth
import controllers.users.update
import controllers.models
import connexion
from openapi_server.models.user_credentials import UserCredentials
from openapi_server.models.update_user import UpdateUser
from journaling import log
from jwt_token import token, JWT_MIN_LENGTH
from controllers.models import PAGE_DEFAULT, PER_PAGE_DEFAULT


#todo use swagger auth not hack with header extraction


def extract_token(authorization):
    authorization = authorization if len(authorization.split()) < 2 else authorization.split()[1]
    #log.debug(f'Auth header: {authorization}')
    return token.decode(authorization)


def get_token(user_credentials=None):  # noqa: E501
    """Get access token for the user

     # noqa: E501

    :param userCredentials:
    :type userCredentials: dict | bytes

    :rtype: Token
    """
    if connexion.request.is_json:
        user_credentials = UserCredentials.from_dict(connexion.request.get_json())  # noqa: E501
    return controllers.users.auth.get_token(
        user_credentials.email,
        user_credentials.password
    )


def create_user(body):  # noqa: E501
    """Create a user

    :rtype: NewUserResponse
    """
    authorization = connexion.request.headers['Authorization']
    new_user = body['new_user'] if 'new_user' in body else body

    return controllers.users.create.create_user(
        auth_token=extract_token(authorization),
        new_user=new_user
    )

def get_user(user_id):  # noqa: E501
    """Info for a specific user

     # noqa: E501

    :param userId: The id of the user to retrieve
    :type userId: str

    :rtype: User
    """
    authorization = connexion.request.headers['Authorization']
    return controllers.users.get.get_user(
        auth_token=extract_token(authorization),
        user_id=user_id
    )


def list_users(per_page: int=PER_PAGE_DEFAULT, page: int=PAGE_DEFAULT):  # noqa: E501
    """List all users

    :param page: Page number of results to return.
    :type page: str
    :param per_page: Number of items on page.
    :type per_page: str

    :rtype: Users
    """
    authorization = connexion.request.headers['Authorization']
    return controllers.users.list.users_list(
        auth_token=extract_token(authorization),
        page=page,
        per_page=per_page
    )


def update_user(user_id, update_user):  # noqa: E501
    """Update details of particular user

     # noqa: E501

    :param user_id: The id of the user to update
    :type user_id: str
    :param update_user:
    :type update_user: dict | bytes

    :rtype: Empty
    """
    authorization = connexion.request.headers['Authorization']
    if connexion.request.is_json:
        update_user = UpdateUser.from_dict(connexion.request.get_json())  # noqa: E501
    return controllers.users.update.update_user(
        auth_token=extract_token(authorization),
        update_user=update_user
    )


def delete_user(userId):  # noqa: E501
    """Delete the user

     # noqa: E501

    :param userId: The id of the user to delete
    :type userId: str

    :rtype: Empty
    """
    authorization = connexion.request.headers['Authorization']
    return controllers.users.delete.delete_user(
        auth_token=extract_token(authorization),
        user_id=userId
    )
