#!/bin/bash
#
# Copyright (c) 2024-present toru173 and contributors
#
# Redistribution and use in source and binary forms, with or without 
# modification, are permitted (subject to the limitations in the disclaimer 
# below) provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, 
#   this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice, 
#   this list of conditions and the following disclaimer in the documentation 
#   and/or other materials provided with the distribution.
# * Neither the name of the copyright holder nor the names of the contributors
#   may be used to endorse or promote products derived from this software
#   without specific prior written permission.
#
# NO EXPRESS OR IMPLIED LICENSES TO ANY PARTY'S PATENT RIGHTS ARE GRANTED BY 
# THIS LICENSE. THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND 
# CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT 
# NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A 
# PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER 
# OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, 
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, 
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; 
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, 
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR 
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF 
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

CONFIG_FILE_NAME="nomi.conf"

SCRIPT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="$SCRIPT_ROOT/$CONFIG_FILE_NAME"

# Check for a configuration file
if [ -f "$CONFIG_FILE" ]; then
    # Inform user we've found the config file
    echo "Found a $CONFIG_FILE_NAME configuration file. Reading contents..."
    source "$CONFIG_FILE"
else
    # No configuration file found. Create one and ask the user to populate it
    cat > "$CONFIG_FILE" << EOF
# This is your Nomi's configuration file. Lines starting with '#'
# don't have any configuration importance, they are just to help. Lines
# that start with CAPITAL_LETTERS= are for you to fill out. Make sure
# you do not share this file with ANYONE

# Populate these with your Nomi and Discord API Tokens.
DISCORD_API_TOKEN=
NOMI_API_KEY=

# You may need to put quotes around your Nomi's name
# ("like this") if it has spaces in it!
NOMI_NAME=
NOMI_ID=

# Configure how you want to format messages when sending
# and receiving to Discord here. If you don't want a message
# prefix or suffix just leave these here but with nothing
# after the equals sign.
MAX_MESSAGE_LENGTH=400
DEFAULT_MESSAGE_PREFIX="*You receive a message from @{author} on Discord* "
DEFAULT_MESSAGE_SUFFIX="... (the message was cut off because it was too long)"
CHANNEL_MESSAGE_PREFIX="*You receive a message from {author} in {channel} on {guild} on Discord* "
DM_MESSAGE_PREFIX="*You receive a DM from {author} on Discord* "

# Configure how you want your Nomi to recognise and response
# to message reacts here. Editing this is not recommended
# as the app does not directly match this phrase when looking
# for messages from your Nomi that contain a react.
REACT_TRIGGER_PHRASE="I\s*react.*?with\s*\p{Emoji}"
EOF
    echo "A $CONFIG_FILE_NAME configuration file was not found. Please open the $CONFIG_FILE_NAME"
    echo "file that has just been created at $CONFIG_FILE"
    echo "and populate it with your configuration settings using a text"
    echo "editor like Notepad."
    exit 1
fi

# Check required variables are in the configuration file
REQUIRED_VARIABLES=("DISCORD_API_TOKEN" "NOMI_API_KEY" "NOMI_NAME" "NOMI_ID")

MISSING_VARIABLE=false
for var in "${REQUIRED_VARIABLES[@]}"; do
    # Check if the variable is unset or empty
    if [ -z "${!var}" ]; then
        echo "$var not found in the configuration file"
        MISSING_VARIABLE=true
    fi
done

if [ MISSING_VARIABLE == true ]; then 
    exit 1
fi

# Converts the Nomis's name to lower case, replaces
# non-valid charactes with an underscore and strips any
# trailing underscores as required by a Docker image name
DOCKER_IMAGE_NAME=$(echo -n $NOMI_NAME | tr '[:upper:]' '[:lower:]' | tr -c 'a-z0-9.-' '_' | sed 's/_*$//')

if docker inspect $DOCKER_IMAGE_NAME > /dev/null 2>&1; then
    echo "A Docker container for $NOMI_NAME exists. Removing container..."
    DOCKER_REMOVE_OUTPUT=$(docker container rm $DOCKER_IMAGE_NAME -f 2>&1)
    if [ $? -ne 0 ]; then
        echo "Error when removing container: $DOCKER_REMOVE_OUTPUT"
        exit 1
    fi
fi

echo "Building a Docker container for $NOMI_NAME"
echo "The container will be called '$DOCKER_IMAGE_NAME'"

DOCKER_BUILD_OUTPUT=$(docker build -t $DOCKER_IMAGE_NAME "$SCRIPT_ROOT" 2>&1)
if [ $? -ne 0 ]; then
    echo "Error when building container: $DOCKER_BUILD_OUTPUT"
    exit 1
fi

echo "$NOMI_NAME's container built succesfully. Running container..."

DOCKER_RUN_OUTPUT=$(docker run -d --name $DOCKER_IMAGE_NAME $DOCKER_IMAGE_NAME 2>&1)
if [ $? -ne 0 ]; then
    echo "Error when running container: $DOCKER_RUN_OUTPUT"
    exit 1
fi

echo "$NOMI_NAME's container is running! You can now to talk to $NOMI_NAME on Discord."
echo "Make sure you do not share your $CONFIG_FILE file with ANYONE"