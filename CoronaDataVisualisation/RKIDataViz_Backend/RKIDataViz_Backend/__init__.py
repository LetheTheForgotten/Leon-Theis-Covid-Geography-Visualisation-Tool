"""
The flask application package.
"""
from RKIDataViz_Backend.Components.Controllers.graphController import graphControllerAPI
from RKIDataViz_Backend.Components.Controllers.baseDataController import baseDataControllerAPI
from flask import Flask
from flask_cors import CORS
import logging

app = Flask(__name__)
app.register_blueprint(graphControllerAPI)
app.register_blueprint(baseDataControllerAPI)

log=logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

cors = CORS(app,resources={r"/api/*":{"origins": "*"}})
import RKIDataViz_Backend.views
