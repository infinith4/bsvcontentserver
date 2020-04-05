from flask import Flask
from flask_bootstrap import Bootstrap

# dictConfig({
#     'version': 1,
#     'formatters': {'default': {
#         'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
#     }},
#     'handlers': {'wsgi': {
#         'class': 'logging.StreamHandler',
#         'stream': 'ext://flask.logging.wsgi_errors_stream',
#         'formatter': 'default'
#     }},
#     'root': {
#         'level': 'INFO',
#         'handlers': ['wsgi']
#     }
# })

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
app.config.from_envvar('FLASK_CONFIG_FILE')
bootstrap = Bootstrap(app)

from flask_pymongo import PyMongo
import dns

app.config["MONGO_URI"] = "mongodb+srv://bsvcontentserver:pallallp5@cluster0-mmmko.mongodb.net/test?retryWrites=true&w=majority"
## https://github.com/mongodb/mongo-python-driver/commit/62400e548db8e02e82afa77b9014d21e47ed2f7c
## query() got an unexpected keyword argument 'lifetime'
## pip3 install dnspython==1.16.0
mongo = PyMongo(app)

import flaskapp.views