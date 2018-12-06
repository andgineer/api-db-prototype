from hypothesis import given
import hypothesis.strategies as st
from journaling import log
import api
import urllib.parse


@given(user_id=st.integers())
def test_delete_fail(user_id, admin_token):
    """
    Tries to delete user in empty DB.
    """
    data = api.users_list(admin_token)
    log.debug('empty db users '+str(data))
    existed_users = set()
    for user in data:
        existed_users.add(user['id'])
    log.debug('existed id '+str(existed_users))
    while str(user_id) in existed_users:
        user_id += 1
    api.delete_user(admin_token, user_id, expected_statuses=[400])
