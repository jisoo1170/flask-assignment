from functools import wraps

from flask import g
from flask_jwt_extended import get_jwt_identity

from app.models.user import User


def login_required(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        user_id = get_jwt_identity()

        try:
            user = User.objects.get(id=user_id)
        except:
            return {'message': '존재하지 않는 사용자입니다'}, 401

        g.user = user
        return func(*args, **kwargs)
    return decorator
