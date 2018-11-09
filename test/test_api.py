from flask import json, url_for
from db import models
from db.db import db


def test_empty_user_list(empty_db, api_client):
    """
    Empty db returns empty user list
    """
    with api_client as client:
        resp = client.get('/users')
        data = json.loads(resp.data)
        assert data['success']
        assert data['result'] == []


def test_user_list(empty_db, api_client, users):
    """
    Creates users and check API request user list
    """
    for user_dict in users:
        user = models.User(**user_dict)
        db.session.add(user)

    with api_client as client:
        resp = client.get('/users')
        data = json.loads(resp.data)
        assert data['success']
        assert len(data['result']) == len(users)
        user_dict = {user['name']: {'email': user['email']} for user in data['result']}
        for user in users:
            assert user['name'] in user_dict
            assert user_dict[user['name']]['email'] == user['email']


def test_user_crud(empty_db, api_client, user):
    """
    Create user, get user list, delete user.
    """
    with api_client as client:
        resp = client.post('/users', data=json.dumps(user), content_type='application/json')
        data = json.loads(resp.data)
        assert isinstance(data, dict) and 'success' in data, f'Create user request fail: {data}'
        assert data['success'], f'Create user request fail: {data}'
        new_user_id = data['result']['id']

        resp = client.get('/users')
        data = json.loads(resp.data)
        assert data['success'], f'Get user list request fail: {data}'
        assert len(data['result']) == 1
        assert data['result'][0]['name'] == user['name']

        resp = client.delete(f'/users/{new_user_id}')
        data = json.loads(resp.data)
        assert isinstance(data, dict) and 'success' in data, f'Delete user request fail: {data}'
        assert data['success'], f'Delete user request fail: {data}'

        resp = client.get('/users')
        data = json.loads(resp.data)
        assert data['success'], f'Get user list request fail: {data}'
        assert len(data['result']) == 0
