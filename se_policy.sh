#!/bin/bash
#PACKAGE=$(yum provides semanage | grep policycoreutils | cut -d ' ' -f1)
#yum install -y $PACKAGE
yum install -y policycoreutils-python-2.5-34.el7.x86_64 2>&1 > /dev/null
/usr/sbin/semanage permissive -a httpd_t