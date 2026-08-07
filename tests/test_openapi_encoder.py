import datetime
from typing import ClassVar

from openapi_server.encoder import JSONEncoder  # use actual import for your JSONEncoder
from openapi_server.models.base_model import Model


class MockModel(Model):
    openapi_types: ClassVar = {"attr1": "type1", "attr2": "type2"}
    attribute_map: ClassVar = {"attr1": "attribute1", "attr2": "attribute2"}

    def __init__(self, attr1, attr2):
        self.attr1 = attr1
        self.attr2 = attr2


def test_JSONEncoder(config):
    encoder = JSONEncoder(config.app)

    # Test with non-Model instance
    non_model_obj = datetime.datetime.now(datetime.timezone.utc)
    assert isinstance(
        encoder.default(non_model_obj), str
    )  # datetime is converted to a string by FlaskJSONEncoder

    # Test with Model instance, include_nulls = False
    model_obj = MockModel("value1", None)
    expected_output = {"attribute1": "value1"}  # Null values are not included
    assert encoder.default(model_obj) == expected_output

    # Test with Model instance, include_nulls = True
    encoder.include_nulls = True
    expected_output = {"attribute1": "value1", "attribute2": None}  # Null values are included
    assert encoder.default(model_obj) == expected_output
