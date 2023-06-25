# coding: utf-8

from __future__ import absolute_import

from datetime import date, datetime  # noqa: F401
from typing import Dict, List  # noqa: F401

from openapi_server import util
from openapi_server.models.base_model_ import Model


class UserGroup(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    """
    allowed enum values
    """
    ADMIN = "admin"
    FULL = "full"
    GUEST = "guest"

    def __init__(self):  # noqa: E501
        """UserGroup - a model defined in OpenAPI"""
        self.openapi_types = {}

        self.attribute_map = {}

    @classmethod
    def from_dict(cls, dikt) -> "UserGroup":
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The UserGroup of this UserGroup.  # noqa: E501
        :rtype: UserGroup
        """
        return util.deserialize_model(dikt, cls)
