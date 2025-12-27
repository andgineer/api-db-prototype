from typing import Any

import controllers.models
import db.conn
import db.models
from controllers.auth import AuthUser
from controllers.helper import api_result, token_to_auth_user, transaction
from journaling import log


# mypy: disallow_untyped_decorators=False
@api_result
@transaction
@token_to_auth_user
def update_user(auth_user: AuthUser, user_id: str, update_user: dict[str, Any]) -> dict[str, Any]:
    """Update user."""
    update_user_obj = controllers.models.UpdateUser(update_user)
    update_user_obj.validate()
    user = db.models.User.by_id(user_id)
    if user.email.lower() != auth_user.email.lower() and not auth_user.is_admin:
        return (  # type: ignore
            f"Only user himself or admin can update user <{user.email}> properties, not <{auth_user.email}>.",
            controllers.models.HttpCode.unauthorized,
        )
    if update_user_obj.email.lower() != user.email.lower():
        return (  # type: ignore
            f"You cannot change user email (current <{user.email}>, new <{update_user_obj.email}>)",
            controllers.models.HttpCode.logic_error,
        )
    update_user_db = update_user_obj.to_orm
    for field in update_user_db:
        setattr(user, field, update_user_db[field])
    db.conn.get_session().commit()
    log.info(f"Updated user [{user}]")
    return update_user_obj.as_dict
