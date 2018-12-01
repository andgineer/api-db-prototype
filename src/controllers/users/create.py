import db.conn
import db.models
from controllers.models import NewUser, HttpCode
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
        return 'Only admin can create users', HttpCode.unauthorized
    new_user = NewUser(new_user)
    new_user.validate()
    user = db.models.User.by_email(new_user.email, check=False)
    if user:
        return f'User with email="{new_user["email"]}" already exists', HttpCode.logic_error
    db_user = db.models.User(**new_user.to_orm)
    db.conn.session.add(db_user)
    db.conn.session.commit()
    log.debug(f'Created user: [{db_user}]')
    return {'id': db_user.id}
