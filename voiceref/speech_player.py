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
from .speech_script import SpeechScript


class SpeechPlayer:
    def __init__(self):
        self._thread_running = False
        self._update_thread = threading.Thread(target=self._update)

        self._script_queue: deque[SpeechScript] = deque()

    def start_playing(self):
        self._thread_running = True
        self._update_thread.start()

    def stop_playing(self):
        self._thread_running = False
        self._update_thread.join()

    def set_scripts(self, scripts: list[SpeechScript]):
        for script in scripts:
            self._script_queue.append(script)

    def _update(self):
        while self._thread_running:
            if len(self._script_queue) == 0:
                time.sleep(0.01)
                continue

            speech_script = self._script_queue.popleft()
            print(speech_script.text)
            time.sleep(speech_script.break_time)
