import db.conn
import db.models


def get_user(user_id):
    try:
        users = db.conn.session.query(db.models.User).filter(db.models.User.id == user_id)
        if not users.count():
            db.session.close()
            return f'No user with id={user_id}', 400
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
    except Exception as e:
        db.conn.session.rollback()
        return f'{e}', 400  # no pretty to send thru api internal exceptions.. just to speed up development
