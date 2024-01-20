# coding: utf-8

from __future__ import absolute_import

from datetime import date, datetime  # noqa: F401
from typing import Dict, List  # noqa: F401

from openapi_server import util
from openapi_server.models.base_model import Model


class Empty(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self):  # noqa: E501
        """Empty - a model defined in Swagger"""
        self.swagger_types = {}

        self.attribute_map = {}

    @classmethod
    def from_dict(cls, dikt) -> "Empty":
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Empty of this Empty.  # noqa: E501
        :rtype: Empty
        """
        return util.deserialize_model(dikt, cls)
