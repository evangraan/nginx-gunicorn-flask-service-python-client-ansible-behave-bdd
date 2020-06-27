#!/bin/bash
ansible -i hosts api -m ping -u ernstv --become --become-user root
