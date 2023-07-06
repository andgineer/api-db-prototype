import controllers.models
import db.conn
import db.models
from controllers.auth import AuthUser
from controllers.helper import api_result, token_to_auth_user, transaction
from controllers.models import HttpCode, UpdateUser
from journaling import log


# mypy: disallow_untyped_decorators=False
@api_result
@transaction
@token_to_auth_user
def update_user(
    auth_user: AuthUser, user_id: str, update_user: UpdateUser
) -> controllers.models.ApiResult:
    """
    Updates user.
    """
    updateUser = controllers.models.UpdateUser(update_user)
    updateUser.validate()
    user = db.models.User.by_id(user_id)
    if user.email.lower() != auth_user.email.lower():
        return (
            f"Only user himself update user <{user.email}> properties, not <{auth_user.email}>.",
            HttpCode.unauthorized,
        )
    if updateUser.email.lower() != user.email.lower():
        return (
            f"You cannot change user email (current <{user.email}>, new <{updateUser.email}>)",
            HttpCode.logic_error,
        )
    updateUser = updateUser.to_orm
    for field in updateUser:
        setattr(user, field, updateUser[field])
    db.conn.session.commit()
    log.info(f"Updated user [{user}]")
