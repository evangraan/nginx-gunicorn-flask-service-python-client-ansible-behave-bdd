import os
import sys
import time
import json
import requests
import logging
import psutil
import threading

def report():
  threading.Timer(5.0, report).start()
  data = []
  for proc in psutil.process_iter(
          ['pid', 'username', 'name', 'status', 'cpu_num', 'num_ctx_switches', 'memory_full_info', 'connections',
           'cmdline', 'create_time', 'ionice', 'num_fds', 'memory_maps', 'cpu_percent', 'terminal', 'ppid', 'cwd',
           'nice', 'cpu_times', 'io_counters', 'memory_info', 'threads', 'open_files', 'num_threads', 'exe', 'uids',
           'gids', 'cpu_affinity', 'memory_percent', 'environ']):
    data.append(proc.info)

  content = {"uuid": config["uuid"], "timestamp": str(time.time()), "data": data}
  headers = {"Content-type": "application/json", "Accept": "text/plain", "Authorization": "Bearer " + config['token']}
  try:
    r = requests.post(url, data=json.dumps(content), headers=headers, verify=False)
    logger.info("Response code: " + str(r.status_code))
    logger.info(r.text)
  except requests.exceptions.RequestException:
    message = "POST failed"
    logger.error(message)

logger = logging.getLogger("client")
logger.setLevel(level=logging.DEBUG)
file_handler = logging.FileHandler("client.log")
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

uuid = config['uuid']
if not uuid:
  message = "client's uuid not configured in config.json"
  logger.error(message)
  sys.exit(message)

url = config['url']
if not url:
  message = "server's url not configured in config.json"
  logger.error(message)
  sys.exit(message)

report()
