# Introduction

This repository contains a reference implementation of the following solution:

* A client instance running CentOS 7
* A server instance running CentOS 7
* The client and server are both provisioned using Ansible
* A python client is scheduled to run every 5 seconds using cron
* The python client retrieves a process list and ships it as JSON to the server API, secured with a bearer token
* A flask API service receives the request and writes the process list to a JSON file
* The flask service is served using gunicorn for WSGI capability and in order to handle high load
* The gunicorn is proxied by Nginx in order to support TLS certificates and port mapping from port 443 to gunicorn
* The solution is integration tested (both the client and the API service) using behave for BDD

# API
```
curl -k -X POST -H 'Authorization: Bearer token-goes-here' -H "Content-Type: application/json" \
  -d '{"uuid" : "a9201032-1e1f-40a2-8995-8472a76dd7d2", "timestamp" : "1593338576.5624585", "data":[ ... ]}' \ 
https://<service-api-IP>/api/v1/record
```

# Security
* The ansible file is provisioned with a login username and password, which is expected to be the same for both servers.
In a production environment, the two servers may have the same username, but passwords should be cycled regularly. Even
better would be to lock the servers down to specific white-listed IPs, disable root login and enable key authentication.
The system ansible is run from then can login without requiring a username and password. 

* The ansible provisioning configures nginx with a self-signed certificate. For production environments this should be
replaced with Certbot (lets-encrypt) once DNS has been configured so that the FQDN for the server resolves correctly.

* Communication with the API service is over SSL and secured using simple bearer token. The token is configured in config.json

# Installation and provisioning
## Ansible configuration and support
* Install ansible
* Install sshpass
* Create a hosts file with both servers' IP addresses and the SSH login username and password. The hosts file in this 
repository  serves as a reference
* Ensure on both servers that the username configured is in the sudoers file (visudo) or in a group that allows sudo

## API Server
```ansible-playbook -i hosts api.yml```

*Note: ssh to the host first so that your ansible system can recognize the ECDSA key fingerprint*

Log into the API server and configure in config.json the record directory and secure token:

```
{
  'records_dir' : 'records',
  'token' : 'somesecuretoken'
}
```

Life-cycle:

```
sudo systemctl stop service
sudo systemctl start service
sudo systemctl restart service
sudo systemctl status service
sudo journalctl -u service
(as root) tail -f /var/log/nginx/*.log /home/<user>/service/service.log
ls -la /home/<user>/service/<records_dir>/
```

## Client

```ansible-playbook -i hosts client.yml```

*Note: ssh to the host first so that your ansible system can recognize the ECDSA key fingerprint*

Log into the client and configure in config.json the node uuid, secure token and API URL:

```
{
  'uuid' : 'a9201032-1e1f-40a2-8995-8472a76dd7d2',
  'token' : 'token-goes-here',
  'url'  : 'https://192.168.1.221/api/v1/record'
}
```

Life-cycle:

```
sudo systemctl stop client
sudo systemctl start client
sudo systemctl restart client
sudo systemctl status client
sudo journalctl -u client
tail -f /home/<user>/client/client.log
```

# Functional overview
## Client application
* The client application captures process information and POSTs it to the service API every 5 seconds
* The client application timestamps records when measurement is taken (seconds since epoch)
* The client application logs to client.log

## API Service
* The API service logs to service.log
* The API service makes use of JSend (https://github.com/omniti-labs/jsend) for its response.
* The API uses the uuid and timestamp fields provided by the client application to store new records. File names follow
the scheme: *uuid*_*timestamp*.json E.g. 3944eb9c-b927-11ea-b3de-0242ac130004_1593338576.5624585.json
* The API service is configured using config.json and records are stored as per the *records_dir* directory.  
* cron is used to schedule cleanup of records older than 1 week to avoid disk space bloat

The server responds with either success:
```{"data":{"timestamp":"1593338576.5624585","uuid":"a9201032-1e1f-40a2-8995-8472a76dd7d2"},"status":"success"}```
or an error:
```{"status":"error", "message":"Could not write to records/3944eb9c-b927-11ea-b3de-0242ac130004_1593338576.5624585.json"}```

# Testing
The API service provides a test API in support of integration testing:

```
flask run

curl -k -X GET -H 'Authorization: Bearer token-goes-here' -H "Content-Type: application/json" http://127.0.0.1:5000/api/test/count

{"data":{"count":1067},"status":"success"}

curl -k -X GET -H 'Authorization: Bearer token-goes-here' -H "Content-Type: application/json" http://127.0.0.1:5000/api/test/latest

{"data":
  {"content":[{"cmdline":["/usr/lib/systemd/systemd","--switched-root","--system","--deserialize","22"],"connections":null,"cpu_affinity":[0],"cpu_num":0,"cpu_percent":0.0,"cpu_times":[0.26,1.23,30.97,13.44,0.09],"create_time":1593293380.06,"cwd":null,"environ":null,"exe":"/usr/lib/systemd/systemd","gids":[0,0,0],"io_counters":null,"ionice":[0,0],"memory_full_info":null,"memory_info":[6782976,131088384,4235264,1454080,0,86323200,0],"memory_maps":null,"memory_percent":0.35194878890086134,"name":"systemd","nice":0,"num_ctx_switches":[2210,3039],"num_fds":null,"num_threads":1,"open_files":null,"pid":1,"ppid":0,"status":"sleeping","terminal":null,"threads":[[1,0.26,1.22]],"uids":[0,0,0],"username":"root"}],
   "filename":"records/development_1593338576.5624585.json"},
 "status":"success"}

```

## Provisioning
* Since provisioning is performed using ansible it is easy to run the ansible playbooks against the client and the
service API. The playbooks report step by step the success or failure of their operation.
* The playbooks are idempotent and can safely be run against systems already operational.
* features/provisioning.feature defines test cases to verify after ansible has successfully completed plays

## Client
* features/client.feature defines all client tests
* These have been manually tested

## Service API
* features/api.feature defines all API tests
* These have been manually tested

## End-to-end integration
* features/integration.feature defines all client tests
* These have been implemented using behave
* On the testing machine: ```pip install behave```
* Add the testing machine's public key to the service API system's .ssh/authorized_keys file
* Configure the IPs and username in features/steps/integration.py
* Run the test suite using:
```
source venv/bin/activate
behave features/integration.feature
```

# Future Improvements
* Split the client and API service into separate git repos (or in the ansible, clone only relevant components)
* Improve the secure token mechanism (e.g. with an injected token obtained from a secure configuration service)
* If DNS is configured and lets-encrypt SSL certificates used, remove "verify=False" from client.py
* Teach ansible to read the service configuration file and set the cleanup period according to a 'keep-records' field
* The service names 'service' and 'client' should be something more meaningful
* Though all tests have been defined, the only tests implemented are integration tests. Automate all tests using 
behave (as per the end-to-end integration example)
* Improve the BDD steps to read the config from hosts and config.py instead of requiring manual entry
* This is a very small project. It is right on the edge of being large enough though to start breaking out classes. If
this grows at all going forward, I'd refactor it.
* There are a couple of ansible work-arounds where ansible did not work as advertised that I'd love to resolve

