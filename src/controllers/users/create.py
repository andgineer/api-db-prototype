from typing import Any

import db.conn
import db.models
from controllers.auth import AuthUser
from controllers.helper import api_result, token_to_auth_user, transaction
from controllers.models import HttpCode, NewUser
from journaling import log


# mypy: disallow_untyped_decorators=False
@api_result
@transaction
@token_to_auth_user
def create_user(auth_user: AuthUser, new_user: dict[str, Any]) -> dict[str, Any]:
    """Create user from dict that contains fields for NewUser.

    Returns {"id": <new user id>}.
    Can return (<error message>, <HTTP code>).
    """
    if not auth_user.is_admin:
        return "Only admin can create users", HttpCode.unauthorized  # type: ignore
    new_user_obj = NewUser(new_user)
    new_user_obj.validate()
    if db.models.User.by_email(new_user_obj.email, check=False):
        return f'User with email="{new_user["email"]}" already exists', HttpCode.logic_error  # type: ignore
    db_user = db.models.User(**new_user_obj.to_orm)
    db.conn.session.add(db_user)  # pyrefly: ignore[missing-attribute]
    db.conn.session.commit()  # pyrefly: ignore[missing-attribute]
    log.debug(f"Created user: [{db_user}]")
    return {"id": db_user.id}
