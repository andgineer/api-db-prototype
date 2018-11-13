import db.conn
import functools
import inspect


SUCCESS_CODE = 200


def transaction(handler):
    """
    Decorator to wrap api handler into try-except to handle DB transaction.
    """
    @functools.wraps(handler)  # preserve initial function signature so tool like transmute continue to work
    def wrapper(*args, **kwargs):
        try:
            return handler(*args, **kwargs)
        except Exception as e:
            db.conn.session.rollback()
            return f'{e}', 400  # todo: internal exception only to log
        finally:
            db.conn.session.close()
    return wrapper


def api_result(handler):
    """
    Decorator to format api handler result.
    Expects from handler tuple with result object and optional code (default 200).
    Formats result as tuple ({'result': <result object>, 'success'}, <code>)
    """
    @functools.wraps(handler)
    def wrapper(*args, **kwargs):
        result = handler(*args, **kwargs)
        if isinstance(result, tuple):
            code = result[1]
            result = result[0]
        else:
            code = SUCCESS_CODE
        return {
            'data': result,
            'success': code == SUCCESS_CODE
        }, code
    wrapper.__signature__ = inspect.signature(handler)
    return wrapper
