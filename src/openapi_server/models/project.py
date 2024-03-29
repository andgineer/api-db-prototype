# coding: utf-8

from __future__ import absolute_import

from datetime import date, datetime  # noqa: F401
from typing import Dict, List, Optional  # noqa: F401

from openapi_server import util
from openapi_server.models.base_model import Model
from openapi_server.models.new_project import NewProject  # noqa: F401,E501


class Project(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, name: Optional[str] = None, id: Optional[str] = None):  # noqa: E501
        """Project - a model defined in Swagger

        :param name: The name of this Project.  # noqa: E501
        :type name: str
        :param id: The id of this Project.  # noqa: E501
        :type id: str
        """
        self.swagger_types = {"name": str, "id": str}

        self.attribute_map = {"name": "name", "id": "id"}

        self._name = name
        self._id = id

    @classmethod
    def from_dict(cls, dikt) -> "Project":
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Project of this Project.  # noqa: E501
        :rtype: Project
        """
        return util.deserialize_model(dikt, cls)

    @property
    def name(self) -> str:
        """Gets the name of this Project.


        :return: The name of this Project.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """Sets the name of this Project.


        :param name: The name of this Project.
        :type name: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def id(self) -> str:
        """Gets the id of this Project.


        :return: The id of this Project.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id: str):
        """Sets the id of this Project.


        :param id: The id of this Project.
        :type id: str
        """

        self._id = id
