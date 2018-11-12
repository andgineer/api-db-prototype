import db.conn
import db.models
from controllers.helper import transaction, api_result


@api_result
@transaction
def delete_user(user_id: str):
    """
    Deletes user.
    Returns deleted user id.
    """
    user_to_delete = db.conn.session.query(db.models.User).filter(db.models.User.id == user_id)
    if user_to_delete.count():
            db.conn.session.delete(user_to_delete.first())
            db.conn.session.commit()
            return None
    else:
        db.conn.session.close()
        return f'No user with id={user_id}', 400

