#!/bin/bash

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