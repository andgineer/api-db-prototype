import db.conn
import db.models
import controllers.models
from controllers.models import NewUser, HttpCode
from controllers.helper import transaction, api_result, token_to_auth_user
from journaling import log
from controllers.models import AuthUser, UpdateUser


@api_result
@transaction
@token_to_auth_user
def update_user(auth_user: AuthUser, user_id, update_user: UpdateUser):
    """
    Updates user.
    """
    updateUser = controllers.models.UpdateUser(update_user)
    updateUser.validate()
    log.debug(f'Going to apply updates {updateUser.as_dict}')
    user = db.models.User.by_id(user_id)
    log.debug(f'found user {user.email}')

