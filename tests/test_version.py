import pytest
from unittest import mock

import version

def test_version():
    # Test when file can be read
    with mock.patch('builtins.open', mock.mock_open(read_data='2023-07-21')) as m:
        assert version.version() == '2023-07-21'
        m.assert_called_once_with("build_timestamp", "r")

    # Test when file read throws an exception
    with mock.patch('builtins.open', side_effect=Exception("Cannot open file")):
        assert version.version() == None
