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

from enum import Enum

TriggerT = str
LangT = str


class TriggerType(Enum):
    NONE = 0
    MATCH = 1
    CHANGED = 2


class SpeechRecipe:
    def __init__(self):
        self.ignored = False
        self.trigger: TriggerT = ""
        self.trigger_type: TriggerType = TriggerType.NONE
        self.trigger_value: int = 0
        self.texts: dict[LangT, list[str]] = {}
