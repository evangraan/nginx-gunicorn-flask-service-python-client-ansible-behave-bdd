import os
import sys
import glob
import json
import time
import logging
import flask
from flask import Flask, request, jsonify
from flask_httpauth import HTTPTokenAuth

app = Flask(__name__)
auth = HTTPTokenAuth(scheme='Bearer')

logger = logging.getLogger("service")
logger.setLevel(level=logging.DEBUG)
file_handler = logging.FileHandler("service.log")
file_handler.setLevel(logging.DEBUG)
logger.addHandler(file_handler)

config_file = 'config.json'
config = {}
if os.path.exists(config_file):
  try:
    with open(config_file) as json_file:
      config = json.load(json_file)
  except [FileNotFoundError, IOError]:
    message = "Could not open configuration file " + config_file
    logger.error(message)
    sys.exit(message)
else:
  message = "Configuration file " + config_file + " does not exist"
  logger.error(message)
  sys.exit(message)

records_dir = config['records_dir']
if not records_dir:
  message = "Storage directory 'records_dir' not configured in config.json"
  logger.error(message)
  sys.exit(message)

if not os.path.exists(records_dir):
  try:
    os.makedirs(records_dir)
  except OSError:
    message = "Could not create storage directory " + records_dir
    logger.error(message)
    sys.exit(message)

@auth.verify_token
def verify_token(token):
  return token == config['token']

@app.route('/api/v1/record', methods=['POST'])
@auth.login_required
def api_record():
  data = request.get_json()
  if data and data['uuid'] and data['timestamp'] and data['data']:
    filename = records_dir + "/" + data['uuid'] + "_" + data['timestamp'] + ".json"
    try:
      with open(filename, "w") as file:
        file.write(json.dumps(data['data']))
      logger.info(data['uuid'] + ": " + data['timestamp'])
    except IOError:
      logger.error("Could not write to " + filename)
      return jsonify({'status' : 'error', 'message' : message})
    return jsonify({'status' : 'success', 'data' : { 'uuid' : data['uuid'], 'timestamp' : data['timestamp'] }})

@app.route('/api/test/count', methods=['GET'])
@auth.login_required
def count_records():
  n = len([name for name in os.listdir(records_dir) if os.path.isfile(os.path.join(records_dir, name))])
  return jsonify({'status' : 'success', 'data' : { 'count' : n}})

@app.route('/api/test/latest', methods=['GET'])
@auth.login_required
def latest_record():
  files = glob.glob(records_dir + '/*.json')
  latest = max(files, key=os.path.getctime)
  data = {'filename': latest}

  try:
    with open(latest) as json_file:
      content = json.load(json_file)
  except [FileNotFoundError, IOError]:
    logger.error("Test API could open record " + latest)
  data['content'] = content

  return jsonify({'status' : 'success', 'data' : data})

if __name__ == "__main__":
  app.run(host='127.0.0.1')

