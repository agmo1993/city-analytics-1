#!/bin/bash

. ./unimelb-comp90024-2020-grp-01-openrc.sh; ansible-playbook --ask-become-pass deploy_swarm.yaml --private-key ~/.ssh/isaac.pem -e 'ansible_python_interpreter=/usr/bin/python3' -i ./inventory/hosts.ini -vvv