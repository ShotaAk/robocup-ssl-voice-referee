#!/usr/bin/env python3

# Copyright 2024 ShotaAk
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import time

from .referee_parser import RefereeParser
from .speech_player import SpeechPlayer
from .speech_script_generator import SpeechScriptGenerator


def main():
    print("Hello, World!")

    while True:
        generator.set_raw_referee(ref_parser.get_raw_referee())

        speech_player.set_scripts(
            generator.stage_scripts(ref_parser.pop_stage()))
        
        # speech_player.set_script(
        #     speech_scripts.command_script(ref_parser.pop_command()))
        
        # speech_player.set_script(
        #     speech_scripts.blue_team_info_script(ref_parser.pop_blue_team_info()))

        # speech_player.set_script(
        #     speech_scripts.yellow_team_info_script(ref_parser.pop_yellow_team_info()))

        time.sleep(0.01)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--referee_addr',
        type=str,
        default='224.5.23.1', help='Set IP address to receive referee command.',
        required=False,
        )
    parser.add_argument(
        '--referee_port',
        type=int,
        default=10003, help='Set IP port to receive referee command.',
        required=False,
        )
    args = parser.parse_args()

    speech_player = SpeechPlayer()
    generator = SpeechScriptGenerator()
    ref_parser = RefereeParser(args.referee_addr, args.referee_port)

    print("Start RoboCup SSL Voice Referee")
    print("    Usage: Ctrl-C to exit\n")

    ref_parser.start_receiving()
    speech_player.start_playing()

    try:
        main()
    except KeyboardInterrupt:
        pass

    speech_player.stop_playing()
    ref_parser.stop_receiving()

    print("\nExit.")
    exit(0)
