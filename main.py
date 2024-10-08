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

from __future__ import annotations
from typing import Optional
from os import environ
from sys import stderr
import re

import discord
from nomi import Session, Nomi

class NomiClient(discord.Client):

    _default_message_prefix = "*You receive a message from {author} on Discord* "
    _default_message_suffix = "... (the message is longer, but was cut off)"
    _default_max_message_length = 400
    _max_max_message_length = 600

    def __init__(self, *, nomi: Nomi, max_message_length: Optional[int] = None, message_prefix: Optional[str] = None, message_suffix: Optional[str] = None, intents: discord.Intents, **options) -> None:
        if type(nomi) is not Nomi:
            raise TypeError(f"Expected nomi to be a Nomi, got a {type(nomi)}")
        
        if message_prefix is not None:
            if type(message_prefix) is not str:
                raise TypeError(f"Expected message_prefix to be a str, got a {type(message_prefix)}")
            self.message_prefix = message_prefix            
        else:
            self.message_prefix = self._default_message_prefix

        if message_suffix is not None:
            if type(message_suffix) is not str:
                raise TypeError(f"Expected message_suffix to be a str, got a {type(message_suffix)}")
            self.message_suffix = message_suffix            
        else:
            self.message_suffix = self._default_message_suffix              

        if max_message_length is None:
            max_message_length = self._default_max_message_length

        if type(max_message_length) is not int:
            raise TypeError(f"Expected max_message_length to be a int, got a {type(max_message_length)}")

        if max_message_length > self._max_max_message_length:
            raise ValueError(f"max_message_length should be equal to or less than {self._max_max_message_length}")
        self.max_message_length = max_message_length      
        
        self._nomi = nomi

        super().__init__(intents, **options)

    def _trim_message(self, message: str) -> str:
        if len(message) <= self.max_message_length:
            return message

        trimmed_message = message[:self.max_message_length + len(self.message_suffix)]
        last_space = trimmed_message.rfind(' ')

        if last_space != -1:
            trimmed_message = trimmed_message[:last_space]

        return trimmed_message + self.message_suffix

    async def on_message(self, discord_message):
        # we do not want the Nomi to reply to themselves
        if discord_message.author.id == self.user.id:
            return

        # Check if the Nomi is mentioned in the message
        if self.user in discord_message.mentions:
            # The Nomi was mentioned. Now check to see if any other users were
            # mentioned, and convert their mention_id to either their displayname
            # or username
            for user in discord_message.mentions:
                # Get the displayname if available, otherwise use the username.
                # If the displayname isn't set this should just be their username.
                name = user.display_name
                mention_id = f"<@{user.id}>"

                # Replace the mention with the displayname
                discord_message_content = discord_message.content.replace(mention_id, name)

            # Build the message to send to the Nomi
            nomi_message = self._message_prefix.format(author = discord_message.author,
                                                       channel = discord_message.channel,
                                                       guild = discord_message.guild)
            
            nomi_message = nomi_message + discord_message_content
            nomi_message = self._trim_message(nomi_message)

            try:
                # Attempt to send message
                _, reply = self._nomi.send_message(nomi_message)
                nomi_reply = reply.text
            except RuntimeError as e:
                # If there's an error, use that as the reply so we can let
                # the user know what went wrong
                nomi_reply = f"❌ ERROR ❌\n{str(e)}"

            # Attempt to substitute user ID in any mentions
            # Example: Replace plain-text @username with the proper mention
            #          format: <@userid>
            # Use a regular expression to find words that start with @
            pattern = r"@(\w+)"
            matches = re.findall(pattern, nomi_reply)

            if matches:
                # Determine if the message is in a DM or a guild
                if discord_message.guild:
                    # If it's a guild, use the guild's member list
                    member_search = lambda name: discord.utils.find(
                        lambda m: m.name.lower() == name.lower() or (m.nick and m.nick.lower() == name.lower()),
                        discord_message.guild.members
                    )
                else:
                    # If it's a DM, use the Nomi's user cache
                    member_search = lambda name: discord.utils.find(
                        lambda u: u.name.lower() == name.lower(),
                        self.users
                    )

                for username in matches:
                    user = member_search(username)
                    if user:
                        mention = f"<@{user.id}>"
                        # Replace @username with the proper mention
                        nomi_reply = nomi_reply.replace(f"@{username}", mention)

            await discord_message.channel.send(nomi_reply)  

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

if __name__ == "__main__":
    # Read variables from config file
    CONFIG_FILE = "nomi.conf"

    CONFIG_VARIABLES = ["DISCORD_API_TOKEN",
                        "NOMI_API_KEY",
                        "NOMI_ID",
                        "MAX_MESSAGE_LENGTH",
                        "MESSAGE_PREFIX",
                        "MESSAGE_SUFFIX",
    ]

    for variable in CONFIG_VARIABLES:
        globals()[variable.lower()] = read_variable_from_file(variable)

    if discord_api_token is None:
        stderr.write("DISCORD_API_TOKEN was not found in the configuration file, or the file was not found")
        exit(1)

    if nomi_api_key is None:
        stderr.write("NOMI_API_KEY was not found in the configuration file, or the file was not found")
        exit(1)

    if nomi_id is None:
        stderr.write("NOMI_ID was not found in the configuration file, or the file was not found")
        exit(1)

    nomi_session = Session(api_key = nomi_api_key)
    nomi = Nomi.from_uuid(session = nomi_session, uuid = nomi_id)        

    intents = discord.Intents.default()
    intents.messages = True
    intents.members = True

    client = NomiClient(nomi = nomi,
                        max_message_length = max_message_length,
                        message_prefix = message_prefix,
                        message_suffix = message_suffix,
                        intents = intents)
    
    client.run(discord_api_token)