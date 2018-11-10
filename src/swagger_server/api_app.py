import connexion
from swagger_server import encoder


app = connexion.App(__name__, specification_dir='./swagger')
app.json_encoder = encoder.JSONEncoder
app.add_api('swagger.yaml', arguments={'title': 'compbiowebAPI'})

