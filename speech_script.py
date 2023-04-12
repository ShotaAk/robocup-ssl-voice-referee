from pathlib import Path
import yaml

class SpeechScript:
    def __init__(self, command, texts):
        self._target_command = command
        self._texts = texts

    def get_target_command(self):
        return self._target_command

    def get_texts(self):
        return self._texts

def load_speech_scripts(target_dir='speech_scripts'):
    # 原稿フォルダにあるすべてのyamlファイルを開き、レフェリーコマンドをキーとした辞書を返す
    speech_script_dict = {}

    for path in Path(target_dir).glob('*.yaml'):
        with open(path) as file:
            obj = yaml.safe_load(file)
            if obj['ignore']:
                continue
            script = SpeechScript(obj['command'], obj['texts'])

            speech_script_dict[script.get_target_command()] = script

    return speech_script_dict
