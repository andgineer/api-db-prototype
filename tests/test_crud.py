from flask import json
import hypothesis.strategies as st
from conftest import get_result_data, DEFAULT_USERS, headers
from hypothesis import given, settings


UserStrategy = st.builds(
  dict,
  name=st.text(),
  email=st.text(),
  password=st.text(min_size=1)
)


@given(random_user=UserStrategy)
@settings(max_examples=10)
def test_user_crud(api_client, random_user, admin_token):
    """
    Create user, get user list, delete user.
    """
    with api_client as client:
        resp = client.post('/users', data=json.dumps(random_user), headers=headers(admin_token))
        data = get_result_data(resp)
        new_user_id = data['id']

        resp = client.get('/users', headers=headers(admin_token))
        data = get_result_data(resp)
        assert len(data) == 1 + DEFAULT_USERS
        for resp_user in data:
            if resp_user['email'] == random_user['email']:
                break
        else:
            assert False, f'Created user [{random_user}] not found in the list [{data}]'

        resp = client.delete(f'/users/{new_user_id}', headers=headers(admin_token))
        get_result_data(resp)  # checks for success

        resp = client.get('/users', headers=headers(admin_token))
        data = get_result_data(resp)
        assert len(data) == DEFAULT_USERS
