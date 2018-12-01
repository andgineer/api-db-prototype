import db.conn
import db.models
from controllers.helper import transaction, api_result, token_to_auth_user
import controllers.models
from controllers.models import AuthUser, HttpCode


@api_result
@transaction
@token_to_auth_user
def get_user(auth_user: AuthUser, user_id):
    """
    Get specific user details
    """
    if not auth_user.is_admin:
        return 'Only admin can get info about user', HttpCode.unauthorized
    users = db.conn.session.query(db.models.User).filter(db.models.User.id == user_id)
    if not users.count():
        return f'No user with id={user_id}', HttpCode.logic_error
    return controllers.models.User().from_orm(users[0]).as_dict
