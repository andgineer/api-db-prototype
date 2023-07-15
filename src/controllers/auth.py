"""Auth controller."""
from typing import Any, Dict

import settings
from controllers.models import APIError, UserGroup
from jwt_token import JWT_EXPIRATION, token

JWT_EMAIL = "sub"
JWT_GROUP = "group"


class AuthUser:
    """User authenticated by JWT from request header."""

    email: str
    group: str

    def __init__(self, token_payload: Dict[str, Any]) -> None:
        """Init the authenticated user from decoded JWT payload.

        Checks expiration.
        """
        assert settings.config
        self.email: str = token_payload[JWT_EMAIL]
        self.group: str = token_payload[JWT_GROUP]
        assert self.group in [group.value for group in UserGroup]
        token_expiration = token.jwt2datetime(token_payload[JWT_EXPIRATION])
        if token_expiration < settings.config.now():
            raise APIError(f"Security token (JWT) had expired at {token_expiration}")

    @property
    def is_admin(self) -> bool:
        """Return True if the user is admin."""
        return UserGroup.ADMIN.value == self.group
