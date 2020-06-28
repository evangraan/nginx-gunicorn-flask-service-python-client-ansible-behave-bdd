# Introduction

This repository contains a reference implementation of the following solution:

* A client instance running CentOS 7
* A server instance running CentOS 7
* The client and server are both provisioned using Ansible
* A python client is scheduled to run every 5 seconds using cron
* The python client retrieves a process list and ships it as JSON to the server API, secured with a secret key
* A flask API service receives the request and writes the process list to a JSON file with the filename = rx timestamp
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

# Functional overview
## Client application
* The client application timestamps records when measurement is taken (seconds since epoch)

## API Service
* The API service makes use of JSend (https://github.com/omniti-labs/jsend) for all responses.
* The API uses the uuid and timestamp fields provided by the client application to store new records. File names follow
the scheme: <uuid>_<timestamp>.json E.g. 3944eb9c-b927-11ea-b3de-0242ac130004_1593338576.5624585.json
* The API service is configured using config.json and records are stored as per the <records_dir> directory.  

The server responds with either success:
```{"data":{"timestamp":"1593338576.5624585","uuid":"a9201032-1e1f-40a2-8995-8472a76dd7d2"},"status":"success"}```
or an error:
```{"status":"error", "message":"Could not write to records/3944eb9c-b927-11ea-b3de-0242ac130004_1593338576.5624585.json"}```



