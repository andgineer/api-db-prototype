def check_token(api_key, required_scopes):
    """
    This function is defined in swagger spec (x-apikeyInfoFunc).

    Actual security check is inside application logic (controllers folder).
    This function is a fake only to please connexion transport.
    """
    return {'uid': ''}
