import connexion
from openapi_server import encoder


app = connexion.App(__name__, specification_dir='./openapi')
app.json_encoder = encoder.JSONEncoder
app.add_api('openapi.yaml', arguments={'title': 'API-prototype'})

