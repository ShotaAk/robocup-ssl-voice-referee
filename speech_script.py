from pathlib import Path
import yaml

class SpeechScripts:
    def __init__(self):
        self._command_scripts = {}
        self._stage_scripts = {}

    def append_command_script(self, command, texts):
        self._command_scripts[command] = texts

    def append_stage_script(self, stage, texts):
        self._stage_scripts[stage] = texts

    def has_script_of_command(self, command):
        return command in self._command_scripts.keys()

    def has_script_of_stage(self, stage):
        return stage in self._stage_scripts.keys()

    def get_script_of_command(self, command):
        return self._command_scripts[command]

    def get_script_of_stage(self, stage):
        return self._stage_scripts[command]


def load_speech_scripts(target_dir='speech_scripts'):
    # target_dirにあるすべてのyamlファイルを開き、原稿オブジェクトspeech_scriptsを作成する
    speech_scripts = SpeechScripts()

    for path in Path(target_dir).glob('*.yaml'):
        with open(path) as file:
            obj = yaml.safe_load(file)
            if obj['ignore']:
                continue

            if obj['trigger'] == 'command':
                speech_scripts.append_command_script(obj['command'], obj['texts'])

            if obj['trigger'] =='stage':
                speech_scripts.append_stage_script(obj['stage'], obj['texts'])

    return speech_scripts
