from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model import Model
from openapi_server.models.user_group import UserGroup
from openapi_server import util

from openapi_server.models.user_group import UserGroup  # noqa: E501

class UpdateUser(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, group=None, email=None, name=None):  # noqa: E501
        """UpdateUser - a model defined in OpenAPI

        :param group: The group of this UpdateUser.  # noqa: E501
        :type group: UserGroup
        :param email: The email of this UpdateUser.  # noqa: E501
        :type email: str
        :param name: The name of this UpdateUser.  # noqa: E501
        :type name: str
        """
        self.openapi_types = {
            'group': UserGroup,
            'email': str,
            'name': str
        }

        self.attribute_map = {
            'group': 'group',
            'email': 'email',
            'name': 'name'
        }

        self._group = group
        self._email = email
        self._name = name

    @classmethod
    def from_dict(cls, dikt) -> 'UpdateUser':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The UpdateUser of this UpdateUser.  # noqa: E501
        :rtype: UpdateUser
        """
        return util.deserialize_model(dikt, cls)

    @property
    def group(self) -> UserGroup:
        """Gets the group of this UpdateUser.


        :return: The group of this UpdateUser.
        :rtype: UserGroup
        """
        return self._group

    @group.setter
    def group(self, group: UserGroup):
        """Sets the group of this UpdateUser.


        :param group: The group of this UpdateUser.
        :type group: UserGroup
        """

        self._group = group

    @property
    def email(self) -> str:
        """Gets the email of this UpdateUser.


        :return: The email of this UpdateUser.
        :rtype: str
        """
        return self._email

    @email.setter
    def email(self, email: str):
        """Sets the email of this UpdateUser.


        :param email: The email of this UpdateUser.
        :type email: str
        """

        self._email = email

    @property
    def name(self) -> str:
        """Gets the name of this UpdateUser.


        :return: The name of this UpdateUser.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """Sets the name of this UpdateUser.


        :param name: The name of this UpdateUser.
        :type name: str
        """

        self._name = name
