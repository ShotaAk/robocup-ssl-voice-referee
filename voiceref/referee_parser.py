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


from collections import deque
import threading
import time
from typing import Deque

from .multicast_receiver import MulticastReceiver
from .proto.ssl_gc_referee_message_pb2 import Referee


class RefereeParser:
    def __init__(
            self,
            referee_addr: str = '224.5.23.1', referee_port: int = 10003) -> None:

        self._receiver = MulticastReceiver(referee_addr, referee_port)
        self._wait_time = 0.01  # msec

        self._thread_running = False
        self._update_thread = threading.Thread(target=self._update)

        self._raw_referee = Referee()
        self._previous_stage: Referee.Stage = None
        self._previous_command: Referee.Command = None
        self._stage_queue: Deque[Referee.Stage] = deque()
        self._command_queue: Deque[Referee.Command] = deque()

    def start_receiving(self) -> None:
        self._thread_running = True
        self._update_thread.start()

    def stop_receiving(self) -> None:
        self._thread_running = False
        self._update_thread.join()

    def get_raw_referee(self) -> Referee:
        return self._raw_referee

    def pop_stage(self) -> Referee.Stage:
        if len(self._stage_queue) == 0:
            return None
        return self._stage_queue.popleft()

    def pop_command(self) -> Referee.Command:
        if len(self._command_queue) == 0:
            return None
        return self._command_queue.popleft()

    def _update(self) -> None:
        while self._thread_running:
            time.sleep(self._wait_time)
            data = self._receiver.receive()
            if data is None:
                continue

            msg = Referee()
            try:
                msg.ParseFromString(data)
                self._raw_referee = msg
                self._set_queue(msg)
            except Exception as e:
                print(e)
                print("Failed to parse message.")

    def _set_queue(self, raw_referee: Referee) -> None:
        # If present data is not same as previous data, append it.
        if self._previous_stage != raw_referee.stage:
            self._stage_queue.append(raw_referee.stage)
            self._previous_stage = raw_referee.stage

        if self._previous_command != raw_referee.command:
            self._command_queue.append(raw_referee.command)
            self._previous_command = raw_referee.command
