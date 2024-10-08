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

# NomiClient Class. This is the main handler
class NomiClient(discord.Client):

    _default_message_prefix = "*You receive a message from {author} on Discord* "
    _default_message_suffix = "... (the message was cut off because it was too long)"
    _default_channel_message_prefix = "*You receive a message from {author} in {channel} on {guild} on Discord* "
    _default_dm_message_prefix = "*You receive a DM from {author} on Discord* "
    _default_react_trigger_phrase = "I react to your message with {emoji}"

    _default_max_message_length = 400
    _max_max_message_length = 600

    _emoji_pattern = (
        "["
        "\U0001F600-\U0001F64F"  # Emoticons
        "\U0001F300-\U0001F5FF"  # Symbols & Pictographs
        "\U0001F680-\U0001F6FF"  # Transport & Map Symbols
        "\U0001F700-\U0001F77F"  # Alchemical Symbols
        "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
        "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
        "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        "\U0001FA00-\U0001FA6F"  # Chess Symbols
        "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
        "\U00002702-\U000027B0"  # Dingbats
        "\U000024C2-\U0001F251" 
        "]+"
    )    

    def __init__(self, *, nomi: Nomi, max_message_length: Optional[int] = None, message_modifiers: dict[str, str], intents: discord.Intents, **options) -> None:
        if type(nomi) is not Nomi:
            raise TypeError(f"Expected nomi to be a Nomi, got a {type(nomi).__name__}")
        
        for modifier, value in message_modifiers.items():
            if value is not None:
                if not isinstance(value, str):
                    raise TypeError(f"Expected message modifier '{modifier}' to be a str, got a {type(value).__name__}")
                # Dynamically set the attribute based on the key
                setattr(self, modifier, value)
            else:
                if modifier != "react_trigger_phrase":
                    setattr(self, modifier, self._default_channel_message_prefix)
                else:
                    setattr(self, modifier, self._default_react_trigger_phrase)

        # Escape the trigger phrase to treat special characters literally
        self.react_trigger_phrase = re.escape(self.react_trigger_phrase)
        
        # Replace escaped asterisks (\*) with \*? to make them optional
        self.react_trigger_phrase = self.react_trigger_phrase.replace(r"\*", r"\*?")
        
        # Replace escaped spaces (\ ) with \s* to make them optional
        self.react_trigger_phrase = self.react_trigger_phrase.replace(r"\ ", r"\s*")                    

        react_trigger_pattern_string = self.react_trigger_phrase.replace(r"\{emoji\}", f"({self._emoji_pattern})")
        self.react_pattern = re.compile(react_trigger_pattern_string)

        if max_message_length is None:
            max_message_length = self._default_max_message_length

        if type(max_message_length) is str:
            try:
                max_message_length = int(max_message_length)
            except:
                raise TypeError(f"Expected max_message_length to be a int, got a {type(max_message_length).__name__}")

        if type(max_message_length) is not int:
            raise TypeError(f"Expected max_message_length to be a int, got a {type(max_message_length).__name__}")

        if max_message_length > self._max_max_message_length:
            raise ValueError(f"max_message_length should be equal to or less than {self._max_max_message_length}")
        self.max_message_length = max_message_length      
        
        self.nomi = nomi

        super().__init__(intents = intents, **options)


    def _trim_message(self, message: str) -> str:
        if len(message) <= self.max_message_length:
            return message

        trimmed_message = message[:self.max_message_length - len(self.default_message_suffix)]
        last_space = trimmed_message.rfind(' ')

        if last_space != -1:
            trimmed_message = trimmed_message[:last_space]

        return trimmed_message + self.default_message_suffix


    async def on_message(self, discord_message):
        # We do not want the Nomi to reply to themselves
        if discord_message.author.id == self.user.id:
            return

        # Check if the Nomi is mentioned in the message, or if we're in DMs
        if self.user in discord_message.mentions or discord_message.guild is None:
            # The Nomi was mentioned (or we're DMing). Now check to see if any other
            # users or roles were mentioned, and convert their mention_id to their
            # username or display name
            discord_message_content = discord_message.content

            for user in discord_message.mentions:
                name = user.display_name if user.display_name else user.name
                mention_id = f"<@{user.id}>"

                # Replace the mention with the user's name
                discord_message_content = discord_message_content.replace(mention_id, name)

            for role in discord_message.role_mentions:
                role_name = role.name
                mention_id = f"<@&{role.id}>"

                # Replace the mention with the role's name
                discord_message_content = discord_message_content.replace(mention_id, role_name)                

            # Set the typing indicator. The Nomi is 'typing' the whole time
            # we are communicating with them, which includes sending the message
            # to the Nomi API, waiting for their response, and sending it back
            # to Discord
            async with discord_message.channel.typing():
                # Build the message to send to the Nomi
                author = discord_message.author
                message_prefix = self.default_message_prefix

                # In DMs channel and guild are None
                if isinstance(discord_message.channel, discord.DMChannel):
                    channel = None
                    guild = None
                    message_prefix = self.dm_message_prefix
                else:
                    channel = discord_message.channel
                    guild = discord_message.guild
                    message_prefix = self.channel_message_prefix

                nomi_message = message_prefix.format(author = author,
                                                    channel = channel,
                                                    guild = guild)
                
                nomi_message = nomi_message + discord_message_content
                nomi_message = self._trim_message(nomi_message)

                try:
                    # Attempt to send message
                    _, reply = self.nomi.send_message(nomi_message)
                    nomi_reply = reply.text
                except RuntimeError as e:
                    # If there's an error, use that as the reply so we can let
                    # the user know what went wrong
                    nomi_reply = f"❌ ERROR ❌\n{str(e)}"

            # Re-set the typing indicator. The Nomi is 'typing' the whole time
            # we are communicating with them, which includes sending the message
            # to the Nomi API, waiting for their response, and sending it back
            # to Discord
            async with discord_message.channel.typing():                    
                # Attempt to substitute user or role ID in any mentions
                # Example: replace the <@userid> or <@&roleid> with the name
                #          of the user or role
                # Use a regular expression to find words that start with @
                pattern = r"@&?(\w+)"
                matches = re.findall(pattern, nomi_reply)

                if matches:
                    # Determine if the message is in a DM or a guild
                    if discord_message.guild:
                        # If it's a guild, use the guild's member list and role list
                        user_or_role_search = lambda name: (
                            discord.utils.find(
                                lambda m: m.name.lower() == name.lower() or (m.nick and m.nick.lower() == name.lower()),
                                discord_message.guild.members
                            ) or discord.utils.find(
                                lambda r: r.name.lower() == name.lower(),
                                discord_message.guild.roles
                            )
                        )
                    else:
                        # If it's a DM, use the Nomi's user cache (roles don't apply in DMs)
                        user_or_role_search = lambda name: discord.utils.find(
                            lambda u: u.name.lower() == name.lower(),
                            self.users
                        )

                    for match in matches:
                        user = user_or_role_search(match)
                        if user:
                            mention = f"<@{user.id}>"
                            # Replace @username or @role with the proper mention
                            nomi_reply = nomi_reply.replace(f"@{match}", mention)
                
                # If the nomi has reacted to the message using the react
                # key phrase, attempt to get that from the Nomi's message
                # and react to our message accordingly
                # Search for the pattern in the text
                match = self.react_pattern.search(nomi_reply)

                # Extract the matched phrase and emoji if found
                if match:
                    trigger_phrase = match.group(0)  # The entire matched text with the emoji
                    emoji = match.group(1)  # The specific emoji captured

                    if trigger_phrase:
                        nomi_reply = nomi_reply.replace(trigger_phrase, '')

                    if emoji:
                        await discord_message.add_reaction(emoji)
                
                # If there's more text, send that as a reply. Don't reply
                # if the Nomi just send at reaction
                if nomi_reply and nomi_reply != "**":
                    await discord_message.channel.send(nomi_reply)  


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
    # Read variables from config file
    CONFIG_FILE = "nomi.conf"

    CONFIG_VARIABLES = ["DISCORD_API_TOKEN",
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
        globals()[variable.lower()] = read_variable_from_file(variable, CONFIG_FILE)

    if discord_api_token is None:
        stderr.write("DISCORD_API_TOKEN was not found in the configuration file, or the file was not found")
        exit(1)

    if nomi_api_key is None:
        stderr.write("NOMI_API_KEY was not found in the configuration file, or the file was not found")
        exit(1)

    if nomi_id is None:
        stderr.write("NOMI_ID was not found in the configuration file, or the file was not found")
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

    client = NomiClient(nomi = nomi,
                        max_message_length = max_message_length,
                        message_modifiers = message_modifiers,
                        intents = intents)
    
    client.run(discord_api_token)