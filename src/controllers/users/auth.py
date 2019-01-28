import db.conn
import db.models
from jwt_token import token, JWT_CREATED, JWT_EXPIRATION
from controllers.helper import transaction, api_result
from controllers.models import HttpCode, APILogicError, APIUnauthError
from controllers.auth import JWT_EMAIL, JWT_GROUP
from journaling import log
import password_hash
import settings


@api_result
@transaction
def get_token(email: str, password: str, auth_token=None):  #todo: remove auth_token
    """
    Returns JWT for the email/password.
    """
    user = db.models.User.by_email(email)
    if not user:
        log.debug(f'No user with email={email}')
        raise APILogicError(f'No user with email={email}')
    if not password_hash.verify(password, user.password_hash):
        log.debug(f'Invalid email/password for user {email}')
        raise APIUnauthError(f'Invalid email/password for user {email}')
    log.debug(f'Issuing JWT for {email}')
    payload = {
        JWT_EXPIRATION: token.datetime2jwt(settings.config.now() + settings.config.token_expiration_delta),
        JWT_CREATED: token.datetime2jwt(settings.config.now()),
        JWT_EMAIL: user.email,
        JWT_GROUP: user.group
    }
    assert '.' not in payload['exp']
    return {'token': token.encode(payload)}
