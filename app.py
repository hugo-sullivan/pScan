from flask import Flask, jsonify, request
import json
from flask_swagger_ui import get_swaggerui_blueprint
import time
import threading
from scan_runner import scan_control_thread
import scan_db
import os
from flasgger import Swagger


app = Flask(__name__)

### swagger specific ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Seans-Python-Flask-REST-Boilerplate"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
### end swagger specific ###

@app.route('/', methods=['POST'])
def new_scan():
    """
    <scan>
    """
    new_scan = json.loads(request.data)
    scan= new_scan["scan"]
    api_key = new_scan["api_key"]
    print(new_scan)
    if (check_valid_key(api_key)):
        scan["scheduled_time"] = (time.time())
        scan_db.add_scan(scan)
        return '200'
    return '400'
    
@app.route('/scheduled/', methods=['GET'])
def get_scheduled():
    return scan_db.get_scheduled_scans()
    
@app.route('/running/', methods=['GET'])
def get_running():
    return scan_db.get_running_scans()

@app.route('/previous/', methods=['GET'])
def get_previous():
    return scan_db.get_previous_scans()

@app.route('/', methods=['DELETE'])
def delete_scan():
    """
    <scan_id>
    """
    delete_scan_id = json.loads(request.data)
    if (check_valid_key(delete_scan_id["api_key"])):
        scan_db.delete_scan(delete_scan_id["id"])
        return '200'    
    return '400'

def check_valid_key(api_key):
    f = open("../configuration.yaml","r")
    for line in f:
        if api_key == line.strip():
            return True
    return False

if __name__ == '__main__':
    
    scan_db.database_init()
    #scan_db.load_db("database.json")
    scan_thread = scan_control_thread()
    scan_thread.start()
    
    app.run(ssl_context=('../cert.pem', '../key.pem'))
    