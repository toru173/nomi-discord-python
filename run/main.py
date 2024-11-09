#!/usr/bin/env python3
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

from typing import Optional

from sys import stderr
import logging
import os

import discord
from nomi import Session, Nomi
from nomi_bot import NomiBot

# Utility Functions
def read_variable_from_file(variable_name: str, filename: str) -> Optional[str]:
    try:
        with open(filename, 'r') as file:
            for line in file:
                # Strip leading/trailing whitespace and newline characters
                line = line.strip()
                # Check if the line starts with the variable name followed by '='
                if line.startswith(f"{variable_name}="):
                    # Return the part after "VARIABLE_NAME="
                    return line[len(f"{variable_name}="):]
        # If the variable is not found, return None
        return None
    except (FileNotFoundError, IOError):
        # Return None if the file cannot be found or read
        return None


def strip_outer_quotation_marks(s: str) -> str:
    # Define a set of unicode-compatible quotation marks to remove
    quote_pairs = {
        '"': '"',
        "'": "'",
        '“': '”',
        '‘': '’',
        '«': '»',
        '‹': '›',
        '„': '“',
        '‚': '‘',
    }

    # Check if the string has at least two characters and the first and last form a valid pair
    if len(s) >= 2 and s[0] in quote_pairs and s[-1] == quote_pairs[s[0]]:
        return s[1:-1]

    return s


if __name__ == "__main__":
    # Read variables from env
    CONFIG_VARIABLES = ["DISCORD_API_KEY",
                        "NOMI_API_KEY",
                        "NOMI_ID",
                        "MAX_MESSAGE_LENGTH",
                        "DEFAULT_MESSAGE_PREFIX",
                        "DEFAULT_MESSAGE_SUFFIX",
                        "CHANNEL_MESSAGE_PREFIX",
                        "DM_MESSAGE_PREFIX",
                        "REACT_TRIGGER_PHRASE",
    ]

    for variable in CONFIG_VARIABLES:
        globals()[variable.lower()] = os.getenv(variable) or None

    if discord_api_key is None:
        logging.error("DISCORD_API_KEY was not found in the configuration file, or the file was not found")
        exit(1)

    if nomi_api_key is None:
        logging.error("NOMI_API_KEY was not found in the configuration file, or the file was not found")
        exit(1)

    if nomi_id is None:
        logging.error("NOMI_ID was not found in the configuration file, or the file was not found")
        exit(1)

    message_modifiers = {
        "default_message_prefix" : default_message_prefix,
        "default_message_suffix" : default_message_suffix,
        "channel_message_prefix" : channel_message_prefix,
        "dm_message_prefix" : dm_message_prefix,
        "react_trigger_phrase" : react_trigger_phrase,
    }

    for modifier, value in message_modifiers.items():
        if value is not None:
            message_modifiers[modifier] = strip_outer_quotation_marks(value)

    nomi_session = Session(api_key = nomi_api_key)
    nomi = Nomi.from_uuid(session = nomi_session, uuid = nomi_id)

    intents = discord.Intents.default()
    intents.messages = True
    intents.members = True

    logging.info("Before creating bot")

    nomi = NomiBot(nomi = nomi,
                   max_message_length = max_message_length,
                   message_modifiers = message_modifiers,
                   intents = intents
                )

    logging.info("Created bot")

    try:
        if running_on_render is not None:
            print("Running on Render. Starting Health Service")
            import http.server
            import threading

            port = os.getenv("PORT")

            class HealthHandler(http.server.BaseHTTPRequestHandler):
                def do_GET(self):
                    self.send_response(200)
                    self.end_headers()

            def start_health_handler():
                server = http.server.HTTPServer(("0.0.0.0", port), HealthHandler)
                print(f"Health check server running on port {port}")
                server.serve_forever()

            health_thread = threading.Thread(target = start_health_handler)
            health_thread.daemon = True
            health_thread.start()
        else:
            print("Not running on Render")
    except NameError:
        print("Not running on Render")

    nomi.run(token = discord_api_key, root_logger = True)
