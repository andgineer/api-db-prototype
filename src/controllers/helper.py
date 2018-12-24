"""
Common code to keep api handler DRY
"""
import db.conn
from journaling import log
from controllers.models import APIError
import re
import inspect
import functools
import traceback
from controllers.models import AuthUser
import schematics.exceptions
from controllers.models import HttpCode


def transaction(handler):
    """
    Decorator to wrap api handler into try-except to handle DB transaction.
    """
    @functools.wraps(handler)
    def wrapper(*args, **kwargs):
        try:
            return handler(*args, **kwargs)
        except APIError as e:
            db.conn.session.rollback()
            log.error(f'{e}')
            return f'API error {e}', HttpCode.wrong_request
        except schematics.exceptions.BaseError as e:
            db.conn.session.rollback()
            messages = []
            for field in e.errors:
                error_messsage = str(e.errors[field]).replace('Rogue', 'Unknown')
                messages.append(f'{field} - {error_messsage}')
            log.error(f'Model validation error: {e}')
            return f'Wrong request parameters: {", ".join(messages)}', HttpCode.wrong_request
        except TypeError as e:
            db.conn.session.rollback()
            missing_args = re.match(r"(.+)missing \d+ required positional argument(s)?: (.+)", str(e))
            if missing_args:
                return f'Missing arguments: {missing_args.group(3)}', HttpCode.wrong_request
            log.error(f'{e}', exc_info=True)
            return 'Server internal error', HttpCode.unhandled_exception
        except Exception as e:
            db.conn.session.rollback()
            log.error(f'{e}', exc_info=True)
            return 'Server internal error', HttpCode.unhandled_exception
        finally:
            db.conn.session.close()
    return wrapper


def api_result(handler):
    """
    Decorator to format api handler result.
    Expects from handler tuple with result object and optional code (default 200).
    Formats result as tuple (<result object>, <http result code>)
    """
    @functools.wraps(handler)
    def wrapper(*args, **kwargs):
        result = handler(*args, **kwargs)
        if isinstance(result, tuple):
            code = result[1]
            result = result[0]
        else:
            code = HttpCode.success
        return result, code
    # Removing our calculated argument auth_user from decorated function
    signature = inspect.signature(handler)
    params = []
    for param in signature.parameters.values():
        if param.name != 'auth_user':
            params.append(param)
    wrapper.__signature__ = signature.replace(parameters=params)
    return wrapper


def token_to_auth_user(handler):
    """
    Creates auth_user parameter from token
    """
    @functools.wraps(handler)  # preserve initial function signature
    def wrapper(*args, **kwargs):
        if 'auth_token' in kwargs:
            if kwargs['auth_token'] is not None:
                args = (AuthUser(kwargs['auth_token']), ) + args
            else:
                log.warning('No or wrong user token in request')
                return 'No or wrong user token in request', HttpCode.no_token
            del kwargs['auth_token']
        return handler(*args, **kwargs)
    return wrapper

