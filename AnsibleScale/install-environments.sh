#!/bin/bash

export ANSIBLE_HOST_KEY_CHECKING=False
. ./unimelb-comp90024-2020-grp-01-openrc.sh; ansible-playbook --ask-become-pass install_environments.yaml -e 'ansible_python_interpreter=/usr/bin/python3' -i inventory/hosts.ini --private-key ~/.ssh/agmo.pem