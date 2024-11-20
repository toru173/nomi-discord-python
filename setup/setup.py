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

import os
import re
import unicodedata
from pathlib import Path

from typing import List, Dict

def normalise_name(name: str) -> str:
    # Normalise to ASCII
    # Remove multiple consequtive spaces, make lower case
    # Remove any characters that aren't a-z, 0-9 or _
    normalised = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('ascii')
    normalised = re.sub(r'\s+', '_', normalised.lower())
    normalised = re.sub(r'[^a-z0-9_]', '', normalised)
    return normalised

def safe_input(prompt: str) -> str:
    while True:
        try:
            return input(prompt)
        except KeyboardInterrupt:
            while True:
                try:
                    response = input("\nSetup is not complete. Do you really want to quit? [y/N]: ").strip().lower()
                    if not response:
                        break
                    if response in ('y', 'yes'):
                        exit(255)
                    elif response in ('n', 'no', ''):
                        break
                    else:
                        print("Please enter 'y' or 'n'.")
                except KeyboardInterrupt:
                    # User must really want to quit. Let them
                    exit(255)

def prompt_user(required_keys: List, current_values: Dict) -> dict:
    user_inputs = {}
    print("Please provide the information needed to configure your Nomi:\n")

    for key in required_keys:
        while True:
            existing_value = current_values.get(key, "")
            if key == "MAX_MESSAGE_LENGTH":
                prompt = f"Are you a paying user? We need to know to set the message length"
                response = safe_input(f"{prompt} [y/N]: ").strip().lower()
                while True:
                    if response in ("yes", "y"):
                        value = 600
                        break
                    elif response in ("no", "n"):
                        value = 400
                        break
                    prompt = f"Please answer yes or no. Are you a paying user?"
                    response = safe_input(f"{prompt} [y/N]: ").strip().lower()
            else:
                prompt = f"{key} [{existing_value}]: " if existing_value else f"{key}: "
                value = safe_input(prompt)
            if value or existing_value:
                break
        user_inputs[key] = value if value else existing_value

    return user_inputs

def replace_placeholders(file_content: str, replacements: Dict[str, str]) -> str:
    for key, value in replacements.items():
        # Replace KEY=VALUE. Handles case where we might have a
        # quote between the equals sign and the var. We need to do
        # things like this to handle the three different ways we can
        # assign vars:
        #  - sh: KEY="VALUE"
        #  - cmd: SET "KEY=VALUE"
        #  - env: KEY=VALUE
        file_content = re.sub(fr'{key}="[^"\s]*', f'{key}="{value}', file_content)
        file_content = re.sub(fr'{key}=(?!")[^"\s]*', f'{key}={value}', file_content)
    return file_content

def main() -> None:

    BOT_PERMISSIONS = "274878122048"

    input_dir = "./"
    output_dir = f"{input_dir}output"

    required_conf_keys = ["DISCORD_API_KEY", "DISCORD_APPLICATION_ID", "NOMI_API_KEY", "NOMI_NAME", "NOMI_ID", "MAX_MESSAGE_LENGTH"]
    placeholder_nomi_name_key = "NOMI_NAME"
    placeholder_docker_image_name = "DOCKER_IMAGE_NAME"

    conf_template_path = Path(f"{input_dir}nomi.conf")
    start_nomi_path = Path(f"{input_dir}start_nomi")

    # Read and parse the .conf file
    with conf_template_path.open("r") as conf_file:
        conf_content = conf_file.read()

    # Extract current values from the .conf content
    # Currently, we are testing this with a new .conf
    # file every time - but I want there to be scope
    # to use this to modify an existing config file
    current_values = {}
    for key in required_conf_keys:
        match = re.search(fr"^{key}=(.*)$", conf_content, flags=re.MULTILINE)
        if match:
            current_values[key] = match.group(1).strip()

    # Prompt user for values, showing current values if they exist
    user_inputs = prompt_user(required_conf_keys, current_values)

    user_inputs["DISCORD_INVITE_URL"] = f"\"https://discord.com/oauth2/authorize?client_id={user_inputs["DISCORD_APPLICATION_ID"]}&permissions={BOT_PERMISSIONS}&integration_type=0&scope=bot\""

    # Normalise the name
    nomi_name = user_inputs["NOMI_NAME"]
    normalised_name = normalise_name(nomi_name)

    # Get file extension based on host OS
    os_type = os.getenv("HOST")
    if "Windows_NT" in os_type:
        extension = ".bat"
    elif "Darwin" in os_type:
        extension = ".command"
    else:
        extension = ".sh"

    modified_conf_content = replace_placeholders(conf_content, user_inputs)


    conf_output_path = Path(f"{output_dir}/{normalised_name}.conf")

    # Write the modified .conf file. There's some weirdness going on
    # here that I think is a race condition, so we just try a couple
    # of times. Debugging will occur in the future, I promise 😅
    try:
        with conf_output_path.open("w") as conf_output_file:
            conf_output_file.write(modified_conf_content)
    except Exception as e:
        print(f"Unable to write to output file: {conf_output_path}")
        print("Please try running setup again")
        print()
        print("@toru173 still hasn't figured out this error. Please post a screentshot")
        print("of the error to help troubleshoot, along with a brief description of")
        print("what happened.")
        print(f"{e}")
        print()
        exit(255)

    # Read start_nomi
    with start_nomi_path.open("r") as start_file:
        start_content = start_file.read()

    # Replace placeholders in start_nomi
    start_replacements = {
        placeholder_nomi_name_key : nomi_name,
        placeholder_docker_image_name : normalised_name
    }

    modified_start_content = replace_placeholders(start_content, start_replacements)

    # Write the modified start_nomi file with the OS-specific extension
    start_output_path = Path(f"{output_dir}/start_{normalised_name}{extension}")
    try:
        with start_output_path.open("w") as start_output_file:
            if "Windows_NT" not in os_type:
                start_output_file.write("#!/usr/bin/env bash\n")
            start_output_file.write(modified_start_content)
    except Exception as e:
        print(f"Unable to write to output file: {start_output_path}")
        print("Please try running setup again")
        print()
        print("@toru173 still hasn't figured out this error. Please post a screentshot")
        print("of the error to help troubleshoot, along with a brief description of")
        print("what happened.")
        print(f"{e}")
        print()
        exit(255)

    print(f"To invite {user_inputs["NOMI_NAME"]} to Discord you can copy and paste the invitation URL")
    print("into a browser:")
    print()
    print(f"{user_inputs["DISCORD_INVITE_URL"].replace("\"", "")}")
    print()

if __name__ == "__main__":
    main()
