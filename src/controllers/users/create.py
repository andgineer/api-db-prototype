import db.conn
import db.models
from controllers.models import NewUser, UNAUTH_OPER_CODE, APP_ERROR_CODE
from controllers.helper import transaction, api_result, token_to_auth_user
from journaling import log
from controllers.models import AuthUser


@api_result
@transaction
@token_to_auth_user
def create_user(auth_user: AuthUser, new_user: dict):
    """
    Creates user.
    Returns new user id.
    """
    if not auth_user.is_admin:
        return 'Only admin can create users', UNAUTH_OPER_CODE
    new_user = NewUser(new_user)
    new_user.validate()
    users = db.conn.session.query(db.models.User).filter(db.models.User.email == new_user.email)
    if users.count():
        return f'User with email="{new_user["email"]}" already exists', APP_ERROR_CODE
    db_user = db.models.User(**new_user.to_orm)
    db.conn.session.add(db_user)
    db.conn.session.commit()
    log.debug(f'Created user: [{db_user}]')
    return {'id': db_user.id}
