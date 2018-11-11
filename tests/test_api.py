from flask import json
import db.conn
import db.models
from hypothesis import settings, strategies, given
import hypothesis.strategies as st

def get_result_data(reply: str) -> dict:
    """
    Parse reply body as json and checks ['success']
    """
    data = json.loads(reply)
    assert isinstance(data, dict) and 'success' in data and data['success'], f'API request fail: {data}'
    return data


def test_empty_user_list(api_client):
    """
    Empty db returns empty user list
    """
    with api_client as client:
        resp = client.get('/users')
        data = get_result_data(resp.data)
        assert data['result'] == []


def test_user_list(api_client, users):
    """
    Creates users and check API request user list
    """
    for user_dict in users:
        user = db.models.User(**user_dict)
        db.conn.session.add(user)

    with api_client as client:
        resp = client.get('/users')
        data = get_result_data(resp.data)
        assert len(data['result']) == len(users)
        user_dict = {user['name']: {'email': user['email']} for user in data['result']}
        for user in users:
            assert user['name'] in user_dict
            assert user_dict[user['name']]['email'] == user['email']


UserStrategy = st.builds(
  dict,
  name=st.text(),
  email=st.text()
)


@given(user=UserStrategy)
def test_user_crud(api_client, user):
    """
    Create user, get user list, delete user.
    """
    with api_client as client:
        resp = client.post('/users', data=json.dumps(user), content_type='application/json')
        data = get_result_data(resp.data)
        new_user_id = data['result']['id']

        resp = client.get('/users')
        data = get_result_data(resp.data)
        assert len(data['result']) == 1
        assert data['result'][0]['name'] == user['name']

        resp = client.delete(f'/users/{new_user_id}')
        data = get_result_data(resp.data)
        assert data['success'], f'Delete user request fail: {data}'

        resp = client.get('/users')
        data = get_result_data(resp.data)
        assert len(data['result']) == 0

