from controllers import db


def delete_user(user_id: str):
    """
    Deletes user.
    Returns deleted user id.
    """
    try:
        user_to_delete = db.session.query(db.models.User).filter(db.models.User.id == user_id)
        if user_to_delete.count():
                db.session.delete(user_to_delete.first())
                db.session.commit()
                return {
                    'result': None,
                    'success': True
                }
        else:
            db.session.close()
            return f'No user with id={id}', 400
    except Exception as e:
        db.session.rollback()
        return f'{e}', 400  # no pretty to send thru api internal exceptions.. just to speed up development
