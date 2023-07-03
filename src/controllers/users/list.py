import controllers.models
import db.conn
import db.models
from controllers.auth import AuthUser
from controllers.helper import api_result, token_to_auth_user, transaction
from controllers.models import PAGE_DEFAULT, PER_PAGE_DEFAULT, APIError, HttpCode, Paging
from journaling import log

DEFAULT_ORDER_BY = "-createdDatetime"


@api_result
@transaction
@token_to_auth_user
def users_list(
    auth_user: AuthUser,
    email: str = None,  # type: ignore  # cannot use Optional because of Transmute auto-swagger magic
    per_page: int = PER_PAGE_DEFAULT,
    page: int = PAGE_DEFAULT,
    order_by=DEFAULT_ORDER_BY,
):
    """
    Users list
    """
    order_by_options = {
        "createddatetime": {"field": "createdDatetime", "model": db.models.User},
        "email": {"field": "email", "model": db.models.User},
    }
    if not auth_user.is_admin:
        return "Only admin can get list of users", HttpCode.unauthorized
    pager = Paging(dict(page=page, per_page=per_page))
    pager.validate()
    if order_by.strip() == "":
        order_by = DEFAULT_ORDER_BY
    if order_by[0] == "-":
        order_by = order_by[1:]
        sort_dir = "desc"
    if order_by[0] == "+":
        order_by = order_by[1:]
    if order_by.lower() not in order_by_options:
        raise APIError(
            f'Wrong order by option "{order_by}". Possible options for order by: {", ".join([key for key in order_by_options.keys()])}'
        )
    sort_by = order_by_options[order_by.lower()]
    order_by = getattr(getattr(sort_by["model"], sort_by["field"]), sort_dir)()
    if email:
        users = [db.models.User.by_email(email, check=False)]
        if users[0] is None:
            users = []
        total = len(users)
    else:
        users = db.models.User.query().order_by(order_by)
        total = users.count()
        users = users.limit(pager.per_page).offset((pager.page - 1) * pager.per_page)
    # db.session..query(db.models.User).from_statement(
    #     text("SELECT * FROM users where name=:name")).\
    #     params(name='john').all()
    result = []
    for user in users:
        result.append(controllers.models.UserShort().from_orm(user).as_dict)
    log.debug(f'List of users: {[user["email"] for user in result]}')
    return {"data": result, "total": total}
