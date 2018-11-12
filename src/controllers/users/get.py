import db.conn
import db.models
from controllers.helper import transaction, api_result


@api_result
@transaction
def get_user(user_id):
    users = db.conn.session.query(db.models.User).filter(db.models.User.id == user_id)
    if not users.count():
        return f'No user with id={user_id}', 400
    result = []
    for user in users:
        result.append({
            'id': str(user.id),
            'name': user.name,
            'email': user.email,
        })
    return result

