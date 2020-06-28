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

# Security
The ansible file is provisioned with a login username and password, which is expected to be the same for both servers.
In a production environment, the two servers may have the same username, but passwords should be cycled regularly. Even
better would be to lock the servers down to specific white-listed IPs, disable root login and enable key authentication.
The system ansible is run from then can login without requiring a username and password. 

The ansible provisioning configures nginx with a self-signed certificate. For production environments this should be
replaced with Certbot (lets-encrypt) once DNS has been configured so that the FQDN for the server resolves correctly.

Communication with the API service is over SSL and secured using simple bearer token. The token is configured in config.json

# Installation and provisioning
## Ansible configuration and support
* Install ansible
* Install sshpass
* Create a hosts file with both servers' IP addresses and the SSH login username and password. The hosts file in this 
repository  serves as a reference
* Ensure on both servers that the username configured is in the sudoers file (visudo) or in a group that allows sudo

## API Server
```ansible-playbook -i hosts api.yml```

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

Log into the client and configure in config.json the node uuid, secure token and API URL:

```
{
  'uuid' : 'a9201032-1e1f-40a2-8995-8472a76dd7d2',
  'token' : 'somesecuretoken',
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

