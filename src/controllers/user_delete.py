import models
import db
from flask import abort
from sqlalchemy.exc import SQLAlchemyError
from transmute_core import APIException
from db import db


def user_delete(id: str):
    """
    Deletes user.
    Returns deleted user id.
    """
    user_to_delete = db.session.query(models.User).filter(models.User.id == id)
    if user_to_delete.count():
        try:
            db.session.delete(user_to_delete.first())
            db.session.commit()
            return {
                'result': None,
                'success': True
            }
        except SQLAlchemyError as e:
            db.session.rollback()
            APIException(f'{e}', code=404)  # no pretty to send thru api internal exceptions.. just to speed up development
    else:
        raise APIException(f'No user with id={id}', code=404)
