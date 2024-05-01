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


import threading
import time

from .multicast_receiver import MulticastReceiver
from .proto.ssl_gc_referee_message_pb2 import Referee


class RefereeParser:
    def __init__(
            self,
            referee_addr: str = '224.5.23.1', referee_port: int = 10003) -> None:

        self._receiver = MulticastReceiver(referee_addr, referee_port)
        self._wait_time = 0.01  # msec

        self._present_referee = Referee()
        self._thread_running = False
        self._update_thread = threading.Thread(target=self._update)

    def start_thread(self) -> None:
        self._thread_running = True
        self._update_thread.start()

    def stop_thread(self) -> None:
        self._thread_running = False
        self._update_thread.join()

    def get_raw_referee(self) -> Referee:
        return self._present_referee

    def _update(self) -> None:
        while self._thread_running:
            time.sleep(self._wait_time)
            data = self._receiver.receive()
            if data is None:
                continue

            msg = Referee()
            try:
                msg.ParseFromString(data)
                self._present_referee = msg
            except Exception as e:
                print(e)
                print("Failed to parse message.")
