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
# * Neither the name of the copyright holder nor the names of its contributors
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

# Check for a .env file, and use the values from there if present
if [ -f ".env" ]; then
    # Load environment variables from .env file
    source ".env"
    echo ".env file found and loaded."
else
    # No .env file found. Create one and ask the user to populate it
    echo "No .env file found. Please open the .env file that has just been created"
    echo "in this folder and populate it with your Nomi and Discord details"
    cat > .env << EOF
# Populate these with your Nomi and Discord details.
# You may need to put quotes around your Nomi's name
# ("like this") if it has spaces in it!
DISCORD_BOT_TOKEN=
NOMI_API_KEY=
NOMI_NAME=
NOMI_ID=
EOF
    exit 1
fi

# Converts the Nomis's name to lower case, replaces
# non-valid charactes with an underscore and strips any
# trailing underscores as required by a Docker image name
DOCKER_IMAGE_NAME=$(echo "$NOMI_NAME" | tr '[:upper:]' '[:lower:]' | tr -c 'a-z0-9.-' '_' | sed 's/_*$//')

SCRIPT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
docker container rm $DOCKER_IMAGE_NAME -f
docker build -t $DOCKER_IMAGE_NAME "$SCRIPT_ROOT"
docker run -d --name $DOCKER_IMAGE_NAME --env-file .env $DOCKER_IMAGE_NAME