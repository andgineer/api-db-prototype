import settings
from controllers.models import APIError, UserGroup
from jwt_token import JWT_EXPIRATION, token

JWT_EMAIL = "sub"
JWT_GROUP = "group"


class AuthUser:
    """
    User authenticated by JWT from request header.
    """

    email: str
    group: str

    def __init__(self, token_payload: dict):
        """
        Init the authenticated user from decoded JWT payload.
        Checks expiration.
        """
        self.email = token_payload[JWT_EMAIL]
        self.group = token_payload[JWT_GROUP]
        token_expiration = token.jwt2datetime(token_payload[JWT_EXPIRATION])
        if token_expiration < settings.config.now():
            raise APIError(f"Security token (JWT) had expired at {token_expiration}")

    @property
    def is_admin(self) -> bool:
        return self.group == UserGroup.ADMIN.value
