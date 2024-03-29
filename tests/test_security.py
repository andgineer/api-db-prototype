import datetime
from datetime import timezone
from string import ascii_letters, digits

from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

import password_hash
from jwt_token import token


@settings(
    max_examples=10, deadline=None, suppress_health_check=[HealthCheck.function_scoped_fixture]
)  # encryption is time consuming and we are not in business to check crypto anyway
@given(st.text(min_size=1, max_size=32, alphabet=ascii_letters + digits), st.text())
def test_jwt_encode(config, key, message):
    payload = {key: message}
    encoded = token.encode(payload)
    assert token.decode(encoded) == payload


@given(st.text())
@settings(
    max_examples=10
)  # hashing is time consuming and we are not in business to check crypto anyway
def test_password_hash(password):
    hashed = password_hash.hash(password)
    assert len(hashed) > 10
    assert password_hash.verify(password, hashed)


def test_jwt_time():
    t = datetime.datetime.now(timezone.utc).replace(microsecond=0)
    assert token.jwt2datetime(token.datetime2jwt(t)) == t
