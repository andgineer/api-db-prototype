import db.conn
import db.models
from controllers.helper import transaction, api_result, token_to_auth_user
from journaling import log
from controllers.models import AuthUser, HttpCode


@api_result
@transaction
@token_to_auth_user
def delete_user(auth_user: AuthUser, user_id: str):
    """
    Deletes user.
    Returns deleted user id.
    """
    if not auth_user.is_admin:
        return 'Only admin can delete users', HttpCode.unauthorized
    user_to_delete = db.conn.session.query(db.models.User).filter(db.models.User.id == user_id)
    if user_to_delete.count():
            log.debug(f'Deletion of user with id={user_id}')
            db.conn.session.delete(user_to_delete.first())
            db.conn.session.commit()
            return None
    else:
        log.debug(f'No user with id={user_id}')
        return f'No user with id={user_id}', HttpCode.logic_error
