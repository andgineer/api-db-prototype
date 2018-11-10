from controllers.models import NewUser
import controllers.users.create


def create_user(**kwargs):
    controllers.users.create.create_user(NewUser(**kwargs))
