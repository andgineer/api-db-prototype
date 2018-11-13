from schematics.models import Model
from schematics.types import StringType


NEW_USER_PARAMS = ['name', 'email']


class NewUser(Model):
    name = StringType(required=True)
    email = StringType(required=True)
    type = StringType()

    @staticmethod
    def _obj_to_dict(obj: object) -> dict:
        return dict(zip(
            NEW_USER_PARAMS,
            [getattr(obj, key) for key in NEW_USER_PARAMS]
        ))

    @property
    def as_dict(self) -> dict:
        return self._obj_to_dict(self)

    @staticmethod
    def from_obj(obj: object):
        new_user = NewUser()
        params = NewUser._obj_to_dict(obj)
        for param in params:
            setattr(new_user, param, params[param])
        return new_user
