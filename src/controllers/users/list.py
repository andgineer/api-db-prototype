import db.conn
import db.models
from controllers.helper import transaction, api_result, token_to_auth_user
import controllers.models
from journaling import log
from controllers.models import AuthUser, Paging, HttpCode


@api_result
@transaction
@token_to_auth_user
def users_list(auth_user: AuthUser, per_page: int=30, page: int=1):
    """
    Users list
    """
    if not auth_user.is_admin:
        return 'Only admin can get list of users', HttpCode.unauthorized
    pager = Paging(dict(page=page, per_page=per_page))
    pager.validate()
    users = db.conn.session.query(db.models.User).limit(pager.per_page).offset((pager.page - 1) * pager.per_page)
    # db.session..query(db.models.User).from_statement(
    #     text("SELECT * FROM users where name=:name")).\
    #     params(name='john').all()
    result = []
    for user in users:
        result.append(controllers.models.UserShort().from_orm(user).as_dict)
    log.debug(f'List of users: {[user["email"] for user in result]}')
    return result
