from flask import Flask, Blueprint
from controllers.users.create import create_user
from controllers.users.delete import delete_user
from controllers.users.list import users_list


app = Flask(__name__)
blueprint = Blueprint("blueprint", __name__, url_prefix="/")

app.add_url_rule('/users/{user_id}', 'delete_user', delete_user, methods=['DELETE'])
app.add_url_rule('/users', 'create_user', create_user, methods=['POST'])
app.add_url_rule('/users', 'users_list', users_list, methods=['GET'])

app.register_blueprint(blueprint)
