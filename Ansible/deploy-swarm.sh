#!/bin/bash

. ./unimelb-comp90024-2020-grp-01-openrc.sh; ansible-playbook -i inventory/hosts.ini -u ubuntu --ask-become-pass deploy_swarm.yaml --private-key ~/.ssh/agmo.pem -e 'ansible_python_interpreter=/usr/bin/python3' -vvv