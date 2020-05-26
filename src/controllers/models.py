from schematics.models import Model
from schematics.types import StringType, IntType, ListType, BaseType
from schematics.exceptions import ConversionError
import enum
import random


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


@enum.unique
class UserGroup(enum.Enum):
    FULL = 'full'
    ADMIN = 'admin'
    GUEST = 'guest'


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


class EnumType(BaseType):
    """
    Converts Python Enum into the string.
    """
    primitive_type = str
    native_type = enum.Enum

    MESSAGES = {
        'convert': ("Couldn't interpret '{0}' value as Enum."),
        'find': 'Couldnt find {value} in {choices}'
    }

    def __init__(self, enum=None, **kwargs):
        self.enum = enum
        super().__init__(**kwargs)

    def _mock(self, context=None):
        return random.choice(list(self.enum.__members__))

    def to_native(self, value, context=None):
        if isinstance(value, self.enum):
            return value
        try:
            for member in self.enum.__members__:
                if member.lower() == value.lower():
                    return self.enum.__members__[member]
            else:
                raise ValueError(self.messages['find'].format(
                    choices=self.enum.__members__, value=value))
        except (ValueError, TypeError):
            raise ConversionError(self.messages['convert'].format(value))

    def to_primitive(self, value, context=None):
        return value.value


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
    group = EnumType(enum=UserGroup)
    email = StringType()
    name = StringType()


class UpdateUser(APIModel):
    group = EnumType(enum=UserGroup)
    email = StringType(required=True)
    password = StringType()
    name = StringType()


class NewUser(APIModel):
    """
    To extend validation https://schematics.readthedocs.io/en/latest/usage/validation.html#extending-validation
    """
    group = EnumType(enum=UserGroup, required=True)
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
    group = EnumType(enum=UserGroup)
    email = StringType()
    name = StringType(default='')


class UserCredentials(APIModel):
  email = StringType()
  password = StringType()


class UsersList(APIModel):
    data = ListType(StringType, required=True)
    total = IntType(required=True)

