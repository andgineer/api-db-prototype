import hypothesis.strategies as st
from hypothesis import HealthCheck, given, settings

import api
from conftest import DEFAULT_USERS

UserStrategy = st.builds(dict, name=st.text(), email=st.text(), password=st.text(min_size=1))


@given(random_user=UserStrategy)
@settings(
    max_examples=10, deadline=None, suppress_health_check=[HealthCheck.function_scoped_fixture]
)
def test_user_crud(random_user, admin_token):
    """
    Create user, get user list, delete user.
    """
    random_user["group"] = "full"
    new_user_id = api.create_user(admin_token, random_user)["id"]

    data = api.users_list(admin_token)
    assert len(data) == 1 + DEFAULT_USERS
    for resp_user in data:
        if resp_user["email"] == random_user["email"]:
            break
    else:
        assert False, f"Created user [{random_user}] not found in the list [{data}]"

    api.delete_user(admin_token, new_user_id)
    assert len(api.users_list(admin_token)) == DEFAULT_USERS

@given(random_user=UserStrategy)
@settings(
    max_examples=10, deadline=None, suppress_health_check=[HealthCheck.function_scoped_fixture]
)
def test_user_crud_update(random_user, admin_token):
    """
    Update user and verify the update.
    """
    random_user["group"] = "full"
    new_user_id = api.create_user(admin_token, random_user)["id"]
    update_user_data = random_user.copy()
    update_user_data["name"] += "Updated name"
    del update_user_data["password"]
    api.update_user(admin_token, update_user_data, new_user_id)
    updated_user = api.get_user(admin_token, new_user_id)
    assert updated_user["name"] == update_user_data["name"], f"Updated user [{update_user_data}] name does not match retrieved user [{updated_user}]"
    assert updated_user["email"] == random_user["email"], f"Updated user [{random_user}] change un-updated field email [{updated_user}]"

    api.delete_user(admin_token, new_user_id)
    assert len(api.users_list(admin_token)) == DEFAULT_USERS
