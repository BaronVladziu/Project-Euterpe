#!/bin/bash
#coding=utf-8

# Strict mode
set -euo pipefail

# Enable remote execution
cd "$(dirname "$0")"

# Create venv
virtualenv -p /usr/bin/python3.6 env

# Run venv
source env/bin/activate

# Print versions
pip3 install --upgrade pip
python3 --version
pip3 --version

# Install python packages
pip3 install -r requirements.txt
