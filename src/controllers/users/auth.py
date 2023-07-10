"""Authenticates a user and returns a JWT token."""
from typing import Any, Dict

import db.conn
import db.models
import password_hash
import settings
from controllers.auth import JWT_EMAIL, JWT_GROUP
from controllers.helper import api_result, transaction
from controllers.models import APILogicError, APIUnauthError
from journaling import log
from jwt_token import JWT_CREATED, JWT_EXPIRATION, token


# mypy: disallow_untyped_decorators=False
@api_result
@transaction
def get_token(
    email: str, password: str, auth_token: Any = None  # pylint: disable=unused-argument
) -> Dict[str, Any]:  # todo: remove auth_token
    """Returns {"token": <JWT for the email/password>}."""
    user = db.models.User.by_email(email)
    if not user:
        log.debug(f"No user with email={email}")
        raise APILogicError(f"No user with email={email}")
    if not password_hash.verify(password, user.password_hash):
        log.debug(f"Invalid email/password for user {email}")
        raise APIUnauthError(f"Invalid email/password for user {email}")
    log.debug(f"Issuing JWT for {email}")
    payload = {
        JWT_EXPIRATION: token.datetime2jwt(
            settings.config.now() + settings.config.token_expiration_delta
        ),
        JWT_CREATED: token.datetime2jwt(settings.config.now()),
        JWT_EMAIL: user.email,
        JWT_GROUP: user.group.value,
    }
    assert "." not in payload["exp"]
    return {"token": token.encode(payload)}
