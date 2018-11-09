from db.db import db
import db.models
from sqlalchemy.exc import SQLAlchemyError
from transmute_core import APIException
from db import db


def user_delete(id: str):
    """
    Deletes user.
    Returns deleted user id.
    """
    db.session.begin()
    try:
        user_to_delete = db.session.query(db.models.User).filter(db.models.User.id == id)
        if user_to_delete.count():
                db.session.delete(user_to_delete.first())
                db.session.commit()
                return {
                    'result': None,
                    'success': True
                }
        else:
            db.session.close()
            raise APIException(f'No user with id={id}', code=404)
    except SQLAlchemyError as e:
        db.session.rollback()
        raise APIException(f'{e}', code=404)  # no pretty to send thru api internal exceptions.. just to speed up development
    except Exception as e:
        db.session.rollback()
        raise APIException(f'{e}', code=404)  # no pretty to send thru api internal exceptions.. just to speed up development
