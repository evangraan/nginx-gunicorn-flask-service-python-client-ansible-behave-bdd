#!/bin/bash
ansible -i hosts centos -m ping -u ernstv --become --become-user root
