from schematics.models import Model
from schematics.types import StringType, IntType, DateTimeType, DateType, ListType


PAGE_DEFAULT = 1
PER_PAGE_DEFAULT = 30


class HttpCode:
    success = 200  # Default HTTP result code
    successes = [success]
    unhandled_exception = 500  # Unhandled exception
    unauthorized = 403
    wrong_request = 501  # Wrong request format etc
    logic_error = 400  # Application level error like user already exists and so on
    no_token = 401  # Request without token for operation that requires one

FULL_ACCESS_GROUP = 'full'
ADMIN_ACCESS_GROUP = 'admin'
GUEST_ACCESS_GROUP = 'guest'


class APIBaseError(Exception):
    status = None  # non-abstract descendants should replace that with specific HTTP error


class APIError(APIBaseError):
    status = HttpCode.wrong_request


class APIUnauthError(APIBaseError):
    status = HttpCode.unauthorized


class APILogicError(APIBaseError):
    status = HttpCode.logic_error


class APIValueError(APIError):
    pass


class APPNoTokenError(APIBaseError):
    pass


class Paging(Model):
    """
    Validation of list's requests page/per_page parameters
    """
    page = IntType(min_value=1, default=PAGE_DEFAULT)
    per_page = IntType(min_value=1, default=PER_PAGE_DEFAULT)

    def __init__(self, raw_data, **kwargs):
        if 'page' in raw_data and str(raw_data['page']).strip() == '':
            del raw_data['page']
        if 'per_page' in raw_data and str(raw_data['per_page']).strip() == '':
            del raw_data['per_page']
        super().__init__(raw_data, **kwargs)


class APIModel(Model):
    @property
    def as_dict(self) -> dict:
        """
        Export with conversion of all fields into safe for json string
        """
        return self.to_primitive()

    @property
    def to_orm(self) -> dict:
        """
        Export for ORM (SQLAlchemy).
        Dictionary without convertion of dates
        """
        result = self.to_native()

        # remove None fields
        empty_fields = set()
        for field in result:
            if result[field] is None:
                empty_fields.add(field)
        for field in empty_fields:
            del result[field]
        return result

    def from_dict(self, data):
        super().__init__({param: data[param] for param in self.keys()})
        return self

    def from_orm(self, data):
        super().__init__({param: getattr(data, param) for param in self.keys()})
        return self


class TokenReply(APIModel):
    """
    get_token reply
    """
    token = StringType(required=True)


class UserShort(APIModel):
    """
    User in list
    """
    id = StringType()
    group = StringType()
    email = StringType()
    name = StringType()


class UpdateUser(APIModel):
    group = StringType()
    email = StringType(required=True)
    password = StringType()
    name = StringType()


class NewUser(APIModel):
    """
    To extend validation https://schematics.readthedocs.io/en/latest/usage/validation.html#extending-validation
    """
    group = StringType(required=True)
    email = StringType(required=True)
    password = StringType(required=True)
    name = StringType()

class NewUserReply(APIModel):
    """
    create rtesult
    """
    id = IntType(required=True)


class User(APIModel):
    id = StringType()
    group = StringType()
    email = StringType()
    name = StringType(default='')


class UserCredentials(APIModel):
  email = StringType()
  password = StringType()


class UsersList(APIModel):
    data = ListType(StringType, required=True)
    total = IntType(required=True)

