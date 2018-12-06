from flask import json
import hypothesis.strategies as st
from conftest import DEFAULT_USERS
import api
from hypothesis import given, settings


UserStrategy = st.builds(
  dict,
  name=st.text(),
  email=st.text(),
  password=st.text(min_size=1)
)


@given(random_user=UserStrategy)
@settings(max_examples=10)
def test_user_crud(random_user, admin_token):
    """
    Create user, get user list, delete user.
    """
    random_user['group'] = 'full'
    new_user_id = api.create_user(admin_token, random_user)['id']

    data = api.users_list(admin_token)
    assert len(data) == 1 + DEFAULT_USERS
    for resp_user in data:
        if resp_user['email'] == random_user['email']:
            break
    else:
        assert False, f'Created user [{random_user}] not found in the list [{data}]'
    api.delete_user(admin_token, new_user_id)
    assert len(api.users_list(admin_token)) == DEFAULT_USERS
