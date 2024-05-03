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


from .proto.ssl_gc_referee_message_pb2 import Referee
from .speech_script import SpeechScript


class SpeechScriptGenerator:
    def __init__(self):
        self._raw_referee = Referee()

    def set_raw_referee(self, raw_referee):
        self._raw_referee = raw_referee

    def stage_scripts(self, stage: Referee.Stage) -> list[SpeechScript]:
        scripts = []

        if stage == Referee.NORMAL_FIRST_HALF:
            scripts.append(SpeechScript("First Half", 1.0))

        return scripts
