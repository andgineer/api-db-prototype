from typing import Any, Dict, Union

import controllers.models
import db.conn
import db.models
from controllers.auth import AuthUser
from controllers.helper import api_result, token_to_auth_user, transaction
from controllers.models import HttpCode


# mypy: disallow_untyped_decorators=False
@api_result
@transaction
@token_to_auth_user
# CI gets types from controllers.model but locally thinks it's untyped, so this `Any` hack to suppress error on return
def get_user(auth_user: AuthUser, user_id: str) -> Union[Dict[str, Any], Any]:
    """Get specific user details."""
    if not auth_user.is_admin:
        return "Only admin can get info about user", HttpCode.unauthorized
    if user := db.models.User.by_id(user_id):
        return controllers.models.User().from_orm(user).as_dict  # pylint: disable=c-extension-no-member
    return f"No user with id={user_id}", HttpCode.logic_error
