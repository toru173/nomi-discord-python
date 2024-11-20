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

import logging

import discord
import regex
from discord.ext import commands
from nomi import Nomi

# NomiBot Class. This is the main handler and includes
# the majority of the custom message-handling logic
class NomiBot(commands.Bot):

    _default_message_prefix = "*You receive a message from @{author} on Discord* "
    _default_message_suffix = "... (the message was cut off because it was too long)"
    _default_channel_message_prefix = "*You receive a message from {author} in {channel} on {guild} on Discord* "
    _default_dm_message_prefix = "*You receive a DM from {author} on Discord* "
    _default_react_trigger_phrase = r"I.*?react.*?with.*?\p{Emoji}.*?"

    _default_max_message_length = 400
    _max_max_message_length = 600

    def __init__(self, *, nomi: Nomi, max_message_length: Optional[int] = None, message_modifiers: dict[str, str], intents: discord.Intents, **options) -> None:
        if type(nomi) is not Nomi:
            raise TypeError(f"Expected nomi to be a Nomi, got a {type(nomi).__name__}")

        self.nomi = nomi
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

        self.react_trigger_pattern = regex.compile(rf"{self.react_trigger_phrase}", regex.IGNORECASE)

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

        super().__init__(command_prefix = "/", intents = intents, **options)


    def _trim_message(self, message: str) -> str:
        if len(message) <= self.max_message_length:
            return message

        trimmed_message = message[:self.max_message_length - len(self.default_message_suffix)]
        last_space = trimmed_message.rfind(' ')

        if last_space != -1:
            trimmed_message = trimmed_message[:last_space]

        return trimmed_message + self.default_message_suffix


    async def on_ready(self):
        logging.info(f"{self.nomi.name} is now online. Happy chatting!")


    async def on_message(self, discord_message):

        # We do not want the Nomi to reply to themselves
        if discord_message.author.id == self.user.id:
            return

        logging.info(f"Received message from Discord: {discord_message}")

        # Check if the Nomi is mentioned in the message, or if we're in DMs
        if self.user in discord_message.mentions or discord_message.guild is None:
            # The Nomi was mentioned (or we're DMing). Now check to see if any other
            # users or roles were mentioned, and convert their mention_id to their
            # username or display name prefixed with an @ symbol
            discord_message_content = discord_message.content

            for user in discord_message.mentions:
                name = user.nick if user.nick else user.display_name
                # Mentions are formatted differently if a user has set a nickname
                if user.nick:
                    mention_id = f"<@!{user.id}>"
                else:
                    mention_id = f"<@{user.id}>"

                # Replace the mention with the user's name
                discord_message_content = discord_message_content.replace(mention_id, f"@{name}")

            for role in discord_message.role_mentions:
                role = role.name
                mention_id = f"<@&{role.id}>"

                # Replace the mention with the role's name
                discord_message_content = discord_message_content.replace(mention_id, f"@{role}")

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
                                                     guild = guild
                                                    )

                nomi_message = nomi_message + discord_message_content
                nomi_message = self._trim_message(nomi_message)

                try:
                    # Attempt to send message
                    _, reply = self.nomi.send_message(nomi_message)
                    nomi_reply = reply.text
                except RuntimeError as e:
                    # If there's an error, use that as the reply so we can let
                    # the user know what went wrong
                    nomi_reply  = f"{self.nomi.name} encountered an error when trying to reply: {str(e)}"

            # Re-set the typing indicator. The Nomi is 'typing' the whole time
            # we are communicating with them, which includes sending the message
            # to the Nomi API, waiting for their response, and sending it back
            # to Discord
            async with discord_message.channel.typing():
                # Attempt to substitute user or role ID in any mentions
                # Example: replace the <@userid>, <!@userid> or <@&roleid> with the name
                #          of the user, the user's nickname or name of the role
                # Use a regular expression to find words that start with @
                matches = regex.findall(r"@&?(\w+)", nomi_reply)

                if matches:
                    # Determine if the message is in a DM or a guild
                    if discord_message.guild:
                        # If it's a guild, use the guild's member list and role list
                        # TODO: Can this be made more efficient with just user.display_name?
                        user_or_role_search = lambda name: (
                            discord.utils.find(
                                lambda m: m.display_name.lower() == name.lower() or (m.nick and m.nick.lower() == name.lower()),
                                discord_message.guild.members
                            ) or discord.utils.find(
                                lambda r: r.name.lower() == name.lower(),
                                discord_message.guild.roles
                            )
                        )
                    else:
                        # If it's a DM, use the Nomi's user cache (roles don't apply in DMs)
                        user_or_role_search = lambda name: discord.utils.find(
                            lambda u: u.display_name.lower() == name.lower(),
                            self.users
                        )

                    for match in matches:
                        user = user_or_role_search(match)
                        if user:
                            mention = f"<@{user.id}>"
                            # Replace @username or @role with the proper mention
                            nomi_reply = nomi_reply.replace(f"@{match}", mention)

                logging.info(f"Sending message to Discord from {self.nomi.name}: {nomi_reply}")

                # If the nomi has reacted to the message using the react
                # key phrase, attempt to get that from the Nomi's message
                # and react to our message accordingly
                # Search for the pattern in the text
                matches = regex.findall(self.react_trigger_pattern, nomi_reply)

                # Extract the matched phrase and emoji if found
                for match in matches:

                    # Look for emojis
                    emojis = regex.findall(r"\p{Emoji}", match)
                    for emoji in emojis:
                        # The regex matches * as an emoji
                        if emoji == "*":
                            continue
                        try:
                            # Attempt to send to Discord
                            await discord_message.add_reaction(emoji)
                        except discord.errors.HTTPException as e:
                            # Check for a specific error code: 10014 (Unknown Emoji)
                            if e.status == 400 and e.code == 10014:
                                logging.error(f"Failed to add reaction: {emoji} is an unknown emoji")
                                # TODO: Figure out a better way to handle a failed react
                                pass
                            else:
                                # Re-raise if it's a different HTTPException
                                raise
                    # Remove the Nomi's react from the text of their reply
                    nomi_reply = regex.sub(match, '', nomi_reply)

                # Clean up the reply message
                nomi_reply = nomi_reply.replace("**", '')
                nomi_reply.strip()

                # If there's more text, send that as a reply. Don't reply
                # if the Nomi just send at reaction
                if nomi_reply:
                    await discord_message.channel.send(nomi_reply)
