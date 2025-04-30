import pytest
import datetime
import typing
from openapi_server.util import _deserialize


class DummyModel:
    openapi_types = {"value": int}
    attribute_map = {"value": "value"}

    def __init__(self):
        self.value = None


class DummyModelNoOpenAPI:
    openapi_types = {"attribute1": str, "attribute2": int}
    attribute_map = {"attribute1": "attribute1", "attribute2": "attribute2"}

    def __init__(self):
        self.attribute1 = None
        self.attribute2 = None


def test_deserialize():
    # Test for None
    assert _deserialize(None, object) is None

    # Test for primitive types
    assert _deserialize("123", int) == 123
    assert _deserialize("123.456", float) == 123.456
    assert _deserialize("true", bool) is True
    assert _deserialize("test string", str) == "test string"

    # Test for date and datetime
    assert _deserialize("2023-07-20", datetime.date) == datetime.date(2023, 7, 20)
    assert _deserialize("2023-07-20T13:45:00", datetime.datetime) == datetime.datetime(
        2023, 7, 20, 13, 45
    )

    # Test for list
    assert _deserialize(["1", "2", "3"], typing.List[int]) == [1, 2, 3]

    # Test for dict
    assert _deserialize({"key1": "1", "key2": "2"}, typing.Dict[str, int]) == {"key1": 1, "key2": 2}

    # Test for model
    assert _deserialize({"value": "1"}, DummyModel).value == 1

    # Test exceptions in _deserialize_primitive
    with pytest.raises(ValueError):
        _deserialize("abc", int)
    with pytest.raises(ValueError):
        _deserialize("abc", float)
    assert _deserialize("abc", str) == "abc"

    # Test for list of model
    data = [{"value": "1"}, {"value": "2"}, {"value": "3"}]
    result = _deserialize(data, typing.List[DummyModel])
    for i in range(3):
        assert result[i].value == i + 1

    # Test for dict of model
    data = {"key1": {"value": "1"}, "key2": {"value": "2"}}
    result = _deserialize(data, typing.Dict[str, DummyModel])
    assert result["key1"].value == 1
    assert result["key2"].value == 2

    # Test for model with no openapi_types
    class DummyModelNoOpenAPI:
        def __init__(self):
            self.value = None

    with pytest.raises(AttributeError):
        result = _deserialize("data", DummyModelNoOpenAPI)
    # obsolete - old version worked also with ValueError
    # assert isinstance(result, DummyModelNoOpenAPI)
    # assert result.value is None


def test_deserialize_model():
    # Set up test data
    data = {"attribute1": "test", "attribute2": 123}

    # Call function
    result = _deserialize(data, DummyModelNoOpenAPI)

    # Check result
    assert isinstance(result, DummyModelNoOpenAPI)
    assert result.attribute1 == "test"
    assert result.attribute2 == 123
