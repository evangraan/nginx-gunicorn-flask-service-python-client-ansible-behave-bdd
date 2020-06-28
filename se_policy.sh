#!/bin/bash
PACKAGE=$(yum provides semanage | grep policycoreutils | cut -d ' ' -f1)
yum install -y $PACKAGE
semanage permissive -a httpd_t