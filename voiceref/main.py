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


def main():
    print("Hello, World!")

    while True:
        stage = ref_parser.pop_stage()
        command = ref_parser.pop_command()
        if stage is not None:
            print("Stage: {}".format(stage))

        if command is not None:
            print("Command: {}".format(command))
        time.sleep(1)


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

    ref_parser = RefereeParser(args.referee_addr, args.referee_port)

    print("Start RoboCup SSL Voice Referee")
    print("    Usage: Ctrl-C to exit\n")

    ref_parser.start_receiving()

    try:
        main()
    except KeyboardInterrupt:
        pass

    ref_parser.stop_receiving()
    print("\nExit.")
    exit(0)
