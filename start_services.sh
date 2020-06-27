#!/bin/bash
systemctl daemon-reload
systemctl restart service
systemctl restart nginx
