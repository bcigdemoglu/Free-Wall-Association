import os
from flask import Flask, jsonify
import flask_restful as restful
from flask_pymongo import PyMongo
from flask import make_response
from bson.json_util import dumps
from hashlib import md5

MONGO_URL = os.environ.get('MONGODB_URI')
if not MONGO_URL:
    MONGO_URL = "mongodb://localhost:27017/local";

app = Flask(__name__)

app.config['MONGO_URI'] = MONGO_URL
app.secret_key = 'kb,v5O,9GBG60^8rg2t;jEy}i63dzZ'
app.mongo = PyMongo(app)

def output_json(obj, code, headers=None):
    resp = make_response(dumps(obj), code)
    resp.headers.extend(headers or {})
    return jsonify(obj)

DEFAULT_REPRESENTATIONS = {'application/json': output_json}
api = restful.Api(app)
api.representations = DEFAULT_REPRESENTATIONS

def hashpwd(password):
    return md5(password.encode('utf-8')).hexdigest()

import resources