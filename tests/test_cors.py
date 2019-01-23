import api
import settings
import pytest


@pytest.mark.no_auto_client
def test_cors(flask_client, admin_token):
    """
    Test Cross Origin Requests settings
    """
    saved_cors = settings.config.web_enableCrossOriginRequests
    try:
        settings.config.web_enableCrossOriginRequests = False
        resp = api.get_options('')
        assert 'Access-Control-Allow-Origin' not in resp.headers
        assert 'Access-Control-Max-Age' not in resp.headers

        api.users_list(admin_token)
        assert 'Access-Control-Allow-Origin' not in api.last_response.headers

        settings.config.web_enableCrossOriginRequests = True
        resp = api.get_options('')
        assert resp.headers['Access-Control-Allow-Origin'] == '*'
        assert 'Access-Control-Max-Age' in resp.headers

        resp = api.get_options('users')
        # Actualy this is just plain response but with headers added in after-request flask hook
        assert resp.headers['Access-Control-Allow-Origin'] == '*'

        api.users_list(admin_token)
        assert api.last_response.headers['Access-Control-Allow-Origin'] == '*'
    finally:
        settings.config.web_enableCrossOriginRequests = saved_cors