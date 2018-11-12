import db.conn


SUCCESS_CODE = 200


def transaction(handler):
    """
    Decorator to wrap api handler into try-except to handle DB transaction.
    """
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
    return wrapper
