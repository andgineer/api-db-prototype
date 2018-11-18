from hypothesis import given
import hypothesis.strategies as st
from journaling import log
from conftest import get_result_data, headers
import urllib.parse


@given(user_id=st.integers())
def test_delete_fail(api_client, user_id, admin_token):
    """
    Tries to delete user in empty DB.
    """
    with api_client as client:
        resp = client.get('/users', headers=headers(admin_token))
        data = get_result_data(resp)
        log.debug('empty db users '+str(data))
        existed_users = set()
        for user in data:
            existed_users.add(user['id'])
        log.debug('existed id '+str(existed_users))
        while str(user_id) in existed_users:
            user_id += 1
        resp = client.delete(f'/users/{urllib.parse.quote(str(user_id))}', headers=headers(admin_token))
        get_result_data(resp, expected_statuses=[400])
