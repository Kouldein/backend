from flask import Flask, Response
from waitress import serve
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from user import user
from events import events
from system import system
from login import login
from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'sfgdhhjftadhsjfhgfsrtvrdgrss'
cors = CORS(app, resources={r"/*": {"origins": "*"}})
jwt = JWTManager(app)
app.register_blueprint(user)
app.register_blueprint(events)
app.register_blueprint(system)
app.register_blueprint(login)

@app.route('/api/v1/hello-world-10')
def myendpoint():
    status_code = Response(response="Hello World 10")
    return status_code

serve(app, host='0.0.0.0', port=8778, threads=1)