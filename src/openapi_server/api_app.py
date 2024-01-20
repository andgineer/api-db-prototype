import connexion

from openapi_server import encoder

app = connexion.App(__name__, specification_dir='./openapi/')
# app.app.json_encoder = encoder.JSONEncoder
app.add_api('openapi.yaml',
            arguments={'title': 'API-prototype'},
            pythonic_params=True)

# @app.app.after_request
# def rewrite_bad_request(response):
#     if response.status_code == 500:  #and response.data.decode('utf-8').find('"title":') != None:
#         log.warning("Holy shit Batman!")
#         # original = loads(response.data.decode('utf-8'))
#         # response.data=dumps({'code': 'VALIDATION_ERROR', 'message': original["detail"]})
#         # response.headers['Content-Type'] = 'application/json'
#     return response
#
#
# def render_unauthorized(exception):
#     return Response(response=json.dumps(
#         {'error': 'There is an error in the oAuth token supplied'}),
#         status=401,
#         mimetype="application/json"
#     )

# app.add_error_handler(Exception, render_unauthorized)
