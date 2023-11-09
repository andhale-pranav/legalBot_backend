#package imports
from flask import Flask
from flask_cors import CORS
import os

#local imports

from routes.response import predict_bp

app = Flask(__name__)

#this is the change

#register the blueprints
# app.register_blueprint(welcome_bp, urel_prefix='')
app.register_blueprint(predict_bp, urel_prefix='')



#setup CORS
CORS(app, origins=['http://localhost:5173'])

if __name__ == '__main__':
    if os.environ.get('ENVIRONMENT') != 'production':
        app.run(host='127.0.0.1', port=8000, debug=True)