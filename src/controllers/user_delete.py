import models
import db
from flask import abort
from sqlalchemy.exc import SQLAlchemyError


def user_delete(id: str) -> str:
    """
    Deletes user
    :param id: user id
    :return: deleted user id
    """
    user_to_delete = db.session.query(models.User).filter(models.User.id == id)
    if user_to_delete.count():
        try:
            db.session.delete(user_to_delete.first())
            db.session.commit()
            return id
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(400, f'{e}')
    else:
        abort(400, f'No user with id={id}')
