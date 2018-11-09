from db.db import db
import db.models
from flask import abort
from sqlalchemy.exc import SQLAlchemyError


def user_create(name: str, email: str):
    """
    Creates user.
    Returns new user id.
    """
    #todo: check uniq name, email?

    try:
        new_user = db.models.User(name=name, email=email)
        db.session.add(new_user)
        db.session.commit()
        return {
            'result': {'id': new_user.id},
            'success': True
        }
    except SQLAlchemyError as e:
        db.session.rollback()
        abort(400, f'{e}')  # no pretty to send thru api internal exceptions.. just to speed up development
