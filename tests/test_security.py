from jwt_token import token
from hypothesis import given, settings
from hypothesis import strategies as st
from string import ascii_letters, digits
import passwords
from journaling import log
import datetime
from datetime import timezone


@settings(max_examples=10)  # encryption is time consuming and we are not in business to check crypto anyway
@given(st.text(min_size=1, max_size=32, alphabet=ascii_letters+digits), st.text())
def test_jwt_encode(config, key, message):
    payload = {key: message}
    encoded = token.encode(payload)
    assert token.decode(encoded) == payload


@given(st.text())
@settings(max_examples=10)  # hashing is time consuming and we are not in business to check crypto anyway
def test_password_hash(password):
    hashed = passwords.hash(password)
    assert len(hashed) > 10
    assert passwords.verify(password, hashed)


def test_jwt_time():
    t = datetime.datetime.now(timezone.utc).replace(microsecond=0)
    assert token.jwt2datetime(token.datetime2jwt(t)) == t
