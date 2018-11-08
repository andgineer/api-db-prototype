import models
import db
from flask import abort
from sqlalchemy.exc import SQLAlchemyError
from flask import jsonify
from db import db


def user_list(per_page: int=10000, page: int=0):
    """
    Users list
    """
    users = db.session.query(models.User).limit(per_page).offset(page * per_page)
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
