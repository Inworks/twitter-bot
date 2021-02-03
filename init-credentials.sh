#! /usr/bin/bash
#  ___   ___  _  _ _ _____   ___ _  _   _   ___ ___
# |   \ / _ \| \| ( )_   _| / __| || | /_\ | _ \ __|
# | |) | (_) | .` |/  | |   \__ \ __ |/ _ \|   / _|
# |___/ \___/|_|\_|   |_|   |___/_||_/_/ \_\_|_\___|
#
# Please double-check that this file is listed in .gitignore before any
# pushes to the GitHub repository.
#
# This bash script is used to set system variables for API keys on execution
# The other Python programs will then search for these environment variables
# and then use them to connect to the respective API services.
#
# In order to execute and access the variables, one must run:
# "source ./init-credentials.sh" in their working directory.

# MakerOS Keys
export PROVIDER_ID=""
export KEY=""
echo "MakerOS API keys successfully initialized."

# Twitter API Keys
export CONSUMER_KEY=""
export CONSUMER_SECRET=""
export ACCESS_TOKEN=""
export ACCESS_TOKEN_SECRET=""
echo "Twitter API keys successfully initialized."
