# coding: utf-8

from __future__ import absolute_import

from datetime import date, datetime  # noqa: F401
from typing import Dict, List  # noqa: F401

from openapi_server import util
from openapi_server.models.base_model_ import Model


class Token(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, token=None):  # noqa: E501
        """Token - a model defined in OpenAPI

        :param token: The token of this Token.  # noqa: E501
        :type token: str
        """
        self.openapi_types = {"token": str}

        self.attribute_map = {"token": "token"}

        self._token = token

    @classmethod
    def from_dict(cls, dikt) -> "Token":
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Token of this Token.  # noqa: E501
        :rtype: Token
        """
        return util.deserialize_model(dikt, cls)

    @property
    def token(self):
        """Gets the token of this Token.

        User jwt token  # noqa: E501

        :return: The token of this Token.
        :rtype: str
        """
        return self._token

    @token.setter
    def token(self, token):
        """Sets the token of this Token.

        User jwt token  # noqa: E501

        :param token: The token of this Token.
        :type token: str
        """

        self._token = token
