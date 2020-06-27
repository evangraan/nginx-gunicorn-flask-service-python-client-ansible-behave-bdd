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

# Installation
## Ansible configuration and support
* Install ansible
* Install sshpass
* Create a hosts file with both servers' IP addresses and the SSH login username and password. The hosts file in this 
repository  serves as a reference
* Ensure on both servers that the username configured is in the sudoers file (visudo)

## Servers
```ansible-playbook -i hosts base.yml```


## Client

## API Service
The API service makes use of JSend (https://github.com/omniti-labs/jsend) for all responses.



