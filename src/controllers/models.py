import enum
import random
from typing import Any, Dict, Optional, Tuple, Type, Union

from schematics.exceptions import ConversionError
from schematics.models import Model
from schematics.types import BaseType, IntType, ListType, StringType

PAGE_DEFAULT = 1
PER_PAGE_DEFAULT = 30

ApiResult = Union[Dict[str, Any], Tuple[str, int]]


class HttpCode:
    """HTTP result codes."""

    success = 200  # Default HTTP result code
    successes = [success]
    unhandled_exception = 500  # Unhandled exception
    unauthorized = 403
    wrong_request = 501  # Wrong request format etc
    logic_error = 400  # Application level error like user already exists and so on
    no_token = 401  # Request without token for operation that requires one


@enum.unique
class UserGroup(enum.Enum):
    """User group."""

    FULL = "full"
    ADMIN = "admin"
    GUEST = "guest"


class APIBaseError(Exception):
    """Error."""

    status: Optional[
        int
    ] = None  # non-abstract descendants should replace that with specific HTTP error


class APIError(APIBaseError):
    """Error."""

    status = HttpCode.wrong_request


class APIUnauthError(APIBaseError):
    """Error."""

    status = HttpCode.unauthorized


class APILogicError(APIBaseError):
    """Error."""

    status = HttpCode.logic_error


class APIValueError(APIError):
    """Error."""


class APPNoTokenError(APIBaseError):
    """Error."""


class Paging(Model):  # type: ignore
    """Validation of list's requests page/per_page parameters."""

    page = IntType(min_value=1, default=PAGE_DEFAULT)
    per_page = IntType(min_value=1, default=PER_PAGE_DEFAULT)

    def __init__(self, raw_data: Dict[str, Any], **kwargs: Any) -> None:
        """Init."""
        if "page" in raw_data and not str(raw_data["page"]).strip():
            del raw_data["page"]
        if "per_page" in raw_data and not str(raw_data["per_page"]).strip():
            del raw_data["per_page"]
        super().__init__(raw_data, **kwargs)


class APIModel(Model):  # type: ignore
    """Model for API responses."""

    @property
    def as_dict(self) -> Dict[str, Any]:
        """Export with conversion of all fields into safe for json string."""
        return self.to_primitive()  # type: ignore

    @property
    def to_orm(self) -> Dict[str, Any]:
        """Export for ORM (SQLAlchemy).

        Dictionary without convertion of dates
        """
        result: Dict[str, Any] = self.to_native()

        empty_fields = {field for field in result if result[field] is None}
        for field in empty_fields:
            del result[field]
        return result

    def from_dict(self, data: Dict[str, Any]) -> "APIModel":
        """Import from dict."""
        super().__init__({param: data[param] for param in self.keys()})
        return self

    def from_orm(self, data: Dict[str, Any]) -> "APIModel":
        """Import from ORM (SQLAlchemy)."""
        super().__init__({param: getattr(data, param) for param in self.keys()})
        return self


class EnumType(BaseType):  # type: ignore
    """Converts Python Enum into the string."""

    primitive_type = str
    native_type = enum.Enum

    MESSAGES = {
        "convert": ("Couldn't interpret '{0}' value as Enum."),
        "find": "Couldnt find {value} in {choices}",
    }

    def __init__(self, enum: Optional[Type[enum.Enum]] = None, **kwargs: Any) -> None:
        """Init."""
        self.enum = enum
        super().__init__(**kwargs)

    def _mock(self, context: Any = None) -> str:
        """Return random enum value."""
        assert self.enum is not None
        return random.choice(list(self.enum.__members__))

    def to_native(self, value: Union[enum.Enum, str], context: Any = None) -> enum.Enum:
        """Convert to native.

        If `value` is instance of `EnumType` return it as it is.
        In other case return `EnumType` instance with name == `value` or raise exception if no such instance.
        """
        assert self.enum is not None
        if isinstance(value, self.enum):
            return value
        if not isinstance(value, str):
            raise ConversionError(self.messages["convert"].format(value))
        assert self.enum is not None
        try:
            for member in self.enum.__members__:
                if member.lower() == value.lower():
                    return self.enum.__members__[member]
            raise ValueError(
                self.messages["find"].format(choices=self.enum.__members__, value=value)
            )
        except (ValueError, TypeError) as e:
            raise ConversionError(self.messages["convert"].format(value)) from e

    def to_primitive(self, value: enum.Enum, context: Any = None) -> Union[str, int]:
        """Convert to primitive."""
        return value.value  # type: ignore


class TokenReply(APIModel):
    """Get_token reply."""

    token = StringType(required=True)


class UserShort(APIModel):
    """User in list."""

    id = StringType()
    group = EnumType(enum=UserGroup)
    email = StringType()
    name = StringType()


class UpdateUser(APIModel):
    """Update user."""

    group = EnumType(enum=UserGroup)
    email = StringType(required=True)
    password = StringType()
    name = StringType()


class NewUser(APIModel):
    """Extend validation.

    https://schematics.readthedocs.io/en/latest/usage/validation.html#extending-validation
    """

    group = EnumType(enum=UserGroup, required=True)
    email = StringType(required=True)
    password = StringType(required=True)
    name = StringType()


class NewUserReply(APIModel):
    """Create result."""

    id = IntType(required=True)


class User(APIModel):
    """User."""

    id = StringType()
    group = EnumType(enum=UserGroup)
    email = StringType()
    name = StringType(default="")


class UserCredentials(APIModel):
    """User credentials."""

    email = StringType()
    password = StringType()


class UsersList(APIModel):
    """List of users."""

    data = ListType(StringType, required=True)
    total = IntType(required=True)
