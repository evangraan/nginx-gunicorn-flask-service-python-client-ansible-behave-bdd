#!/bin/bash
systemctl daemon-reload
systemctl restart service
systemctl restart nginx
#systemctl enable is supposed to do the symlinks below, but it does not from ansible, so do it here
ln -s /usr/lib/systemd/system/nginx.service /etc/systemd/system/multi-user.target.wants/nginx.service
ln -s /etc/systemd/system/service.service /etc/systemd/system/multi-user.target.wants/service.service