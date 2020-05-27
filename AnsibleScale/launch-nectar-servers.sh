#!/bin/bash

. ./unimelb-comp90024-2020-grp-01-openrc.sh; ansible-playbook --ask-become-pass launch_nectar.yaml -e 'ansible_python_interpreter=/usr/bin/python3' -i inventory/hosts.ini