# coding: utf-8

from __future__ import absolute_import

from datetime import date, datetime  # noqa: F401
from typing import Dict, List  # noqa: F401

from openapi_server import util
from openapi_server.models.base_model import Model


class UserToShareWith(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, email=None):  # noqa: E501
        """UserToShareWith - a model defined in OpenAPI

        :param email: The email of this UserToShareWith.  # noqa: E501
        :type email: str
        """
        self.openapi_types = {"email": str}

        self.attribute_map = {"email": "email"}

        self._email = email

    @classmethod
    def from_dict(cls, dikt) -> "UserToShareWith":
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The UserToShareWith of this UserToShareWith.  # noqa: E501
        :rtype: UserToShareWith
        """
        return util.deserialize_model(dikt, cls)

    @property
    def email(self):
        """Gets the email of this UserToShareWith.

        email of user to share with  # noqa: E501

        :return: The email of this UserToShareWith.
        :rtype: str
        """
        return self._email

    @email.setter
    def email(self, email):
        """Sets the email of this UserToShareWith.

        email of user to share with  # noqa: E501

        :param email: The email of this UserToShareWith.
        :type email: str
        """

        self._email = email
