#!/bin/bash
systemctl daemon-reload
systemctl restart client
#systemctl enable is supposed to do the symlinks below, but it does not from ansible, so do it here
ln -s /usr/lib/systemd/system/client.service /etc/systemd/system/multi-user.target.wants/client.service