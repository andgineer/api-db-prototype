import db.conn
import db.models


def users_list(type: str=None, per_page: int=10000, page: int=0):
    """
    Users list
    """
    users = db.conn.session.query(db.models.User).limit(per_page).offset(page * per_page)
    # db.session..query(db.models.User).from_statement(
    #     text("SELECT * FROM users where name=:name")).\
    #     params(name='john').all()
    result = []
    for user in users:
        result.append({
            'id': str(user.id),
            'name': user.name,
            'email': user.email,
        })
    return {
      "success": True,
      "result": result
    }
