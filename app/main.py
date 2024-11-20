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
import os

import http.server
import http.client
import threading

import discord
from nomi import Session, Nomi
from nomi_bot import NomiBot

# Utility Functions
def strip_outer_quotation_marks(quoted_string: str) -> str:
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
    if len(quoted_string) >= 2 and quoted_string[0] in quote_pairs and quoted_string[-1] == quote_pairs[quoted_string[0]]:
        return quoted_string[1:-1]

    return quoted_string


def get_env_vars() -> dict:
    # Read variables from env
    REQUIRED_ENV_VARS = ["DISCORD_API_KEY",
                            "NOMI_API_KEY",
                            "NOMI_ID",
                            "MAX_MESSAGE_LENGTH",
                            "DEFAULT_MESSAGE_PREFIX",
                            "DEFAULT_MESSAGE_SUFFIX",
                            "CHANNEL_MESSAGE_PREFIX",
                            "DM_MESSAGE_PREFIX",
                            "REACT_TRIGGER_PHRASE",
                            "RENDER_EXTERNAL_URL"
                    ]
    env = {}
    for var in REQUIRED_ENV_VARS:
        env[var.lower()] = os.getenv(var) or None

    return env


# Functions for dealing with Render
def health_handler() -> None:
    # We just need to return a '200' on any request to PORT to
    # prove we're healthy. Absolutely minimal setup here.
    class HealthHandler(http.server.BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            if self.path == "/health":
                os.sys.stderr.write("Received health check-in 💊\n")
                # Respond to the health check with 200 ('OK')
                self.send_response(200)
                self.end_headers()

        def do_HEAD(self) -> None:
            self.send_response(200)
            self.end_headers()

        # Suppress logging the health check
        def log_message(self, format, *args):
            return

    port = int(os.getenv("PORT") or -1)
    if port < 0: return

    os.sys.stderr.write("Starting health handler\n")
    with http.server.HTTPServer(('0.0.0.0', port), HealthHandler) as server:
        server.serve_forever()
    os.sys.stderr.write("Shutting down health handler\n")


def heartbeat_handler() -> None:
    # We need to be world-reachable and have something
    # interact with the app every 15 minutes otherwise
    # we get spun down
    class HeartbeatHandler(http.server.BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            if self.path == "/heartbeat":
                os.sys.stderr.write("Received heartbeat check-in ♥️\n")
                # Respond to the heartbeat check with 200 ('OK')
                self.send_response(200)
                self.end_headers()

        def do_HEAD(self) -> None:
            self.send_response(200)
            self.end_headers()

        # Suppress logging the health check
        def log_message(self, format, *args):
            return

    os.sys.stderr.write("Starting heartbeat handler\n")
    with http.server.HTTPServer(('0.0.0.0', 443), HeartbeatHandler) as server:
        server.serve_forever()
    os.sys.stderr.write("Shutting down heartbeat handler\n")


def heartbeat() -> None:
    # Here we set a timer to check our heartbeat
    os.sys.stderr.write("Starting heartbeat service\n")
    threading.Timer(800, heartbeat).start()

    render_external_url = os.getenv("RENDER_EXTERNAL_URL" or None)
    if render_external_url is None:
        os.sys.stderr.write("Could not get URL of Render Service\n")
        return

    # Strip leading protocol indicator
    render_external_url = render_external_url.replace('https://', '')
    render_external_url = render_external_url.replace('http://', '')

    try:
        os.sys.stderr.write("Checking heartbeat 🩺\n")
        conn = http.client.HTTPSConnection(render_external_url)
        conn.request("GET", "/heartbeat")
        body = conn.getresponse().read()
        status = conn.getresponse().status
        if status == 200:
            os.sys.stderr.write(f"We have a heartbeat ♥️\n")
        else:
            os.sys.stderr.write(f"Could not get heartbeat 😰\n")
            os.sys.stderr.write(f"Body:\n{body}\n")
    except Exception as e:
        print(f"Unable to check for heartbeat: {e}")


def main() -> None:

    env = get_env_vars()

    if env["discord_api_key"] is None:
        os.sys.stderr.write("DISCORD_API_KEY was not found in the environment variables\n")
        exit(1)

    if env["nomi_api_key"] is None:
        os.sys.stderr.write("NOMI_API_KEY was not found in the environment variables\n")
        exit(1)

    if env["nomi_id"] is None:
        os.sys.stderr.write("NOMI_ID was not found in the environment variables\n")
        exit(1)

    message_modifiers = {
        "default_message_prefix" : env["default_message_prefix"],
        "default_message_suffix" : env["default_message_suffix"],
        "channel_message_prefix" : env["channel_message_prefix"],
        "dm_message_prefix" : env["dm_message_prefix"],
        "react_trigger_phrase" : env["react_trigger_phrase"],
    }

    for modifier, value in message_modifiers.items():
        if value is not None:
            message_modifiers[modifier] = strip_outer_quotation_marks(value)

    nomi_session = Session(api_key = env["nomi_api_key"])
    nomi = Nomi.from_uuid(session = nomi_session, uuid = env["nomi_id"])

    intents = discord.Intents.default()
    intents.members = True
    intents.messages = True
    intents.message_content = True

    nomi = NomiBot(nomi = nomi,
                   max_message_length = env["max_message_length"],
                   message_modifiers = message_modifiers,
                   intents = intents
                )

    # Check if we're running on Render. We need to do
    # some housekeeping if we are, including responding
    # to health checks and keeping the service running.
    if env["render_external_url"] is not None:
        os.sys.stderr.write("Running on Render. Starting health and heartbeat handlers...\n")
        health_handler_thread = threading.Thread(target = health_handler)
        heartbeat_handler_thread = threading.Thread(target = heartbeat_handler)
        heartbeat_thread = threading.Thread(target = heartbeat)

        health_handler_thread.daemon = True
        heartbeat_handler_thread.daemon = True
        heartbeat_thread.daemon = True

        health_handler_thread.start()
        heartbeat_handler_thread.start()
        heartbeat_thread.start()

    nomi.run(token = env["discord_api_key"], root_logger = True)


if __name__ == "__main__":
    main()
