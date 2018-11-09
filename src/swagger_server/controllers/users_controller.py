import connexion
from sqlalchemy.exc import SQLAlchemyError
from swagger_server.models.new_user import NewUser as swaggerNewUser  # noqa: E501
from swagger_server.models.new_user_response import NewUserResponse  # noqa: E501
from swagger_server.models.user import User  # noqa: E501
from swagger_server.models.users import Users  # noqa: E501
from swagger_server import util
from db.db import db
from db import models


def create_user(NewUser):  # noqa: E501
    """Create a user

     # noqa: E501

    :param NewUser:
    :type NewUser: dict | bytes

    :rtype: NewUserResponse
    """
    if connexion.request.is_json:
        NewUser = swaggerNewUser.from_dict(connexion.request.get_json())  # noqa: E501
    try:
        new_user = models.User(name=NewUser.name, email=NewUser.email)
        db.session.add(new_user)
        db.session.commit()
        return {
            'result': {'id': new_user.id},
            'success': True
        }
    except SQLAlchemyError as e:  # speatial treatment for SQLAlchemy errors?
        db.session.rollback()
        return f'{e}', 400  # no pretty to send thru api internal exceptions.. just to speed up development
    except Exception as e:
        db.session.rollback()
        return f'{e}', 400  # no pretty to send thru api internal exceptions.. just to speed up development


def get_user(userId):  # noqa: E501
    """Info for a specific user

     # noqa: E501

    :param userId: The id of the user to retrieve
    :type userId: str

    :rtype: User
    """
    try:
        users = db.session.query(models.User).filter(models.User.id == userId)
        if not users.count():
            db.session.close()
            return f'No user with id={userId}', 400
        result = []
        for user in users:
            result.append({
                'id': str(user.id),
                'name': user.name,
                'email': user.email,
            })
        return {
            "success": True,
            "result": result
        }
    except SQLAlchemyError as e:  # speatial treatment for SQLAlchemy errors?
        db.session.rollback()
        return f'{e}', 400  # no pretty to send thru api internal exceptions.. just to speed up development
    except Exception as e:
        db.session.rollback()
        return f'{e}', 400  # no pretty to send thru api internal exceptions.. just to speed up development


def list_users(type=None, page=0, per_page=10000):  # noqa: E501
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
    try:
        users = db.session.query(models.User).limit(per_page).offset(page * per_page)
        result = []
        for user in users:
            result.append({
                'id': str(user.id),
                'name': user.name,
                'email': user.email,
            })
        return {
            "success": True,
            "result": result
        }
    except SQLAlchemyError as e:  # speatial treatment for SQLAlchemy errors?
        db.session.rollback()
        return f'{e}', 400  # no pretty to send thru api internal exceptions.. just to speed up development
    except Exception as e:
        db.session.rollback()
        return f'{e}', 400  # no pretty to send thru api internal exceptions.. just to speed up development


def delete_user(userId):  # noqa: E501
    """Delete the user

     # noqa: E501

    :param userId: The id of the user to delete
    :type userId: str

    :rtype: Empty
    """
    try:
        user_to_delete = db.session.query(models.User).filter(models.User.id == userId)
        if not user_to_delete.count():
            db.session.close()
            return f'No user with id={id}', 400
        db.session.delete(user_to_delete.first())
        db.session.commit()
        return {
            'result': None,
            'success': True
        }
    except SQLAlchemyError as e:  # speatial treatment for SQLAlchemy errors?
        db.session.rollback()
        return f'{e}', 400  # no pretty to send thru api internal exceptions.. just to speed up development
    except Exception as e:
        db.session.rollback()
        return f'{e}', 400  # no pretty to send thru api internal exceptions.. just to speed up development
