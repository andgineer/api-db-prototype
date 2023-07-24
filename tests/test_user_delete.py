import hypothesis
import hypothesis.strategies as st
from hypothesis import HealthCheck

import api
from journaling import log


@hypothesis.given(user_id=st.integers())
@hypothesis.settings(
    max_examples=10, deadline=None, suppress_health_check=[HealthCheck.function_scoped_fixture]
)
def test_delete_fail(user_id, admin_token):
    """Delete user in empty DB."""
    data = api.users_list(admin_token)
    log.debug(f"empty db users {str(data)}")
    existing_user_ids = {user["id"] for user in data}
    log.debug(f"existed id {existing_user_ids}")
    non_existing_user_id = max((int(id) for id in existing_user_ids), default=user_id) + 1
    api.delete_user(admin_token, non_existing_user_id, expected_statuses=[400])
