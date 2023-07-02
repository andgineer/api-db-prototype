"""
Common code to keep api handler DRY
"""
import functools
import inspect
import re
from typing import Any, Callable, Concatenate, Dict, ParamSpec, TypeVar, cast

import schematics.exceptions
from mypy_extensions import KwArg, VarArg

import db.conn
import journaling
from controllers.auth import AuthUser
from controllers.models import APIBaseError, HttpCode
from journaling import log
from pretty_ns import time_ns

TCallable = TypeVar("TCallable", bound=Callable[[VarArg(Any), KwArg(Any)], Any])


def transaction(handler: TCallable) -> TCallable:
    """Decorate api handler into try-except to handle DB transaction."""

    @functools.wraps(handler)
    def transaction_wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return handler(*args, **kwargs)
        except APIBaseError as e:
            db.conn.session.rollback()
            log.error(f"{e}")
            return f"API error {e}", e.status
        except schematics.exceptions.BaseError as e:
            db.conn.session.rollback()
            messages = []
            for field in e.errors:
                error_messsage = str(e.errors[field]).replace("Rogue", "Unknown")
                messages.append(f"{field} - {error_messsage}")
            log.error(f"Model validation error: {e}")
            return f'Wrong request parameters: {", ".join(messages)}', HttpCode.wrong_request
        except TypeError as e:
            db.conn.session.rollback()
            missing_args = re.match(
                r"(.+)missing \d+ required positional argument(s)?: (.+)", str(e)
            )
            if missing_args:
                return f"Missing arguments: {missing_args[3]}", HttpCode.wrong_request
            log.error(f"{e}", exc_info=True)
            return "Server internal error", HttpCode.unhandled_exception
        except Exception as e:
            db.conn.session.rollback()
            log.error(f"{e}", exc_info=True)
            return "Server internal error", HttpCode.unhandled_exception
        finally:
            db.conn.session.close()

    return cast(TCallable, transaction_wrapper)


def api_result(handler: TCallable) -> TCallable:
    """Decorate api handler result.

    Expects from handler tuple with result object and optional code (default 200).
    Formats result as tuple (<result object>, <http result code>)
    """

    @functools.wraps(handler)
    def api_result_wrapper(*args: Any, **kwargs: Any) -> Any:
        journaling.request_start_time = time_ns()
        try:
            result = handler(*args, **kwargs)
            if isinstance(result, tuple):
                code = result[1]
                result = result[0]
            else:
                code = HttpCode.success
            return result, code
        finally:
            journaling.request_start_time = None

    # Removing our calculated argument auth_user from decorated function
    signature = inspect.signature(handler)
    params = []
    for param in signature.parameters.values():
        if param.name != "auth_user":
            params.append(param)
    # suppress "Callable[[VarArg(Any), KwArg(Any)], Any]" has no attribute "__signature__"
    api_result_wrapper.__signature__ = signature.replace(parameters=params)  # type: ignore[attr-defined]
    return cast(TCallable, api_result_wrapper)


P = ParamSpec("P")
R = TypeVar("R")


def token_to_auth_user(handler: Callable[Concatenate[Dict[str, Any], P], R]) -> Callable[P, R]:
    """Create auth_user parameter from token."""

    @functools.wraps(handler)  # preserve initial function signature
    def token_to_auth_user_wrapper(*args: Any, **kwargs: Any) -> Any:
        if "auth_token" in kwargs:
            if kwargs["auth_token"] is not None:
                log.debug(f'Add auth_user to {handler.__name__}\n{kwargs["auth_token"]}')
                auth_user = AuthUser(kwargs["auth_token"])
                args = (auth_user,) + args
                journaling.user = auth_user.email
            else:
                log.warning("No or wrong user token in request")
                return "No or wrong user token in request", HttpCode.no_token
            del kwargs["auth_token"]
        try:
            return handler(*args, **kwargs)
        finally:
            journaling.user = None

    # suppress "Callable[[VarArg(Any), KwArg(Any)], Any]" has no attribute "__signature__"
    token_to_auth_user_wrapper.__signature__ = inspect.signature(handler)  # type: ignore[attr-defined]
    return token_to_auth_user_wrapper
