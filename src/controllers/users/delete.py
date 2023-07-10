import db.conn
import db.models
from controllers.auth import AuthUser
from controllers.helper import api_result, token_to_auth_user, transaction
from controllers.models import HttpCode
from journaling import log


# mypy: disallow_untyped_decorators=False
@api_result
@transaction
@token_to_auth_user
def delete_user(auth_user: AuthUser, user_id: str):  # type: ignore  # transmute Swagger magic does not allow type hints
    """Delete user.

    Returns deleted user id.
    """
    if not auth_user.is_admin:
        return "Only admin can delete users", HttpCode.unauthorized
    if user_to_delete := db.models.User.by_id(user_id, check=False):
        log.debug(f"Deletion of user with id={user_id}")
        db.conn.session.delete(user_to_delete)
        db.conn.session.commit()
        return {}
    log.debug(f"No user with id={user_id}")
    return f"No user with id={user_id}", HttpCode.logic_error
