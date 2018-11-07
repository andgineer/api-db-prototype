import models
import db
from flask import abort
from sqlalchemy.exc import SQLAlchemyError


def user_create(name: str, email: str) -> int:
    """
    Creates user
    :param name: user name
    :param email: user email
    :return: new user id
    """
    #todo: check uniq name, email?
    try:
        new_user = models.User(name=name, email=email)
        db.session.add(new_user)
        db.session.commit()
        return new_user.id
    except SQLAlchemyError as e:
        db.session.rollback()
        abort(400, f'{e}')
