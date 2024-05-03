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
from .speech_recipe import SpeechRecipe
from .speech_script import SpeechScript
from pathlib import Path
import yaml


TriggerT = str


class SpeechScriptGenerator:
    def __init__(self):
        self._raw_referee = Referee()
        self._recipes: dict[TriggerT, SpeechRecipe] = {}

    def load_recipes(self, recipe_dir: str) -> bool:
        loaded = False
        for path in Path(recipe_dir).rglob("*.yaml"):
            result, recipe = self._verify_recipe(path)

            if result:
                self._recipes[recipe.trigger] = recipe
                loaded = True
        return loaded

    def set_raw_referee(self, raw_referee):
        self._raw_referee = raw_referee

    def stage_scripts(self, stage: Referee.Stage) -> list[SpeechScript]:
        scripts = []

        if stage == Referee.NORMAL_FIRST_HALF:
            scripts.append(SpeechScript("First Half", 1.0))

        return scripts

    def _verify_recipe(self, file_path: str) -> tuple[bool, SpeechRecipe]:
        if not Path(file_path).exists():
            print("File {} does not exist.".format(file_path))
            return False, None

        opened_file = open(file_path, "r")
        recipe = yaml.safe_load(opened_file)

        success = True
        speech_recipe = SpeechRecipe()
        error_msg = "File {} does not have fields:".format(file_path)

        if "ignored" in recipe:
            speech_recipe.ignored = recipe["ignored"]
        else:
            error_msg += "ignored, "
            success = False

        if "trigger" in recipe:
            speech_recipe.trigger = recipe["trigger"]
        else:
            error_msg += "trigger, "
            success = False

        if "trigger_type" in recipe:
            speech_recipe.trigger_type = recipe["trigger_type"]
        else:
            error_msg += "trigger_type, "
            success = False

        if "trigger_value" in recipe:
            speech_recipe.trigger_value = recipe["trigger_value"]

        for lang, texts in recipe["texts"].items():
            speech_recipe.texts[lang] = texts

        if not success:
            print(error_msg)

        return success, speech_recipe
