import connexion
from swagger_server.models.new_user import NewUser as swaggerNewUser  # noqa: E501
from swagger_server.models.new_user_response import NewUserResponse  # noqa: E501
from swagger_server.models.user import User  # noqa: E501
from swagger_server.models.users import Users  # noqa: E501
import controllers.users.create
import controllers.users.delete
import controllers.users.get
import controllers.users.list
import controllers.models


def create_user(NewUser: swaggerNewUser):  # noqa: E501
    """Create a user

     # noqa: E501

    :param NewUser:
    :type NewUser: dict | bytes

    :rtype: NewUserResponse
    """
    if connexion.request.is_json:
        NewUser = swaggerNewUser.from_dict(connexion.request.get_json())  # noqa: E501
    PARAMS = ['type', 'name', 'email']
    return controllers.users.create.create_user(controllers.models.NewUser(
        **dict(zip(PARAMS, [getattr(NewUser, key) for key in PARAMS]))))

def get_user(userId):  # noqa: E501
    """Info for a specific user

     # noqa: E501

    :param userId: The id of the user to retrieve
    :type userId: str

    :rtype: User
    """
    return controllers.users.get.get_user(userId)


def list_users(**kwargs):  # noqa: E501
    """List all users

     # noqa: E501

    :param type: The type of user to retrieve
    :type type: str
    :param page: Page number of results to return.
    :type page: str
    :param per_page: Number of items on page.
    :type per_page: str

    :rtype: Users
    """
    return controllers.users.list.users_list(**kwargs)


def delete_user(userId):  # noqa: E501
    """Delete the user

     # noqa: E501

    :param userId: The id of the user to delete
    :type userId: str

    :rtype: Empty
    """
    return controllers.users.delete.delete_user(userId)
