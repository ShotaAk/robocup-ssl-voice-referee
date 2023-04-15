from functools import reduce
from pathlib import Path
import yaml

class SpeechScript:
    def __init__(self, texts, parameters):
        self._texts = texts
        self._parameters = []
        if parameters is not None:
            self._parameters = parameters

    def get_texts(self, referee_msg):
        # textsにセットされた文字列にformat処理を実行して返す
        parameters = self._extract_parameters(referee_msg)
        return list(map(lambda x: x.format(*parameters), self._texts))

    def _extract_parameters(self, referee_msg):
        # parametersにセットされた属性をreferee_msgから抽出する
        parameters = []
        for param_str in self._parameters:
            param_str_list = param_str.split('.')
            parameters.append(
                reduce(lambda obj, attr: getattr(obj, attr),
                       param_str_list, referee_msg))
        return parameters

class SpeechScripts:
    def __init__(self):
        self._command_scripts = {}
        self._stage_scripts = {}

    def append_command_script(self, command, texts, parameters):
        self._command_scripts[command] = SpeechScript(texts, parameters)

    def append_stage_script(self, stage, texts, parameters):
        self._stage_scripts[stage] = SpeechScript(texts, parameters)

    def has_script_of_command(self, command):
        return command in self._command_scripts.keys()

    def has_script_of_stage(self, stage):
        return stage in self._stage_scripts.keys()

    def get_script_of_command(self, command, referee_msg):
        return self._command_scripts[command].get_texts(referee_msg)

    def get_script_of_stage(self, stage, referee_msg):
        return self._stage_scripts[stage].get_texts(referee_msg)


def load_speech_scripts(target_dir='speech_scripts'):
    # target_dirにあるすべてのyamlファイルを開き、原稿オブジェクトspeech_scriptsを作成する
    speech_scripts = SpeechScripts()

    for path in Path(target_dir).glob('**/*.yaml'):
        with open(path) as file:
            obj = yaml.safe_load(file)
            if obj['ignore']:
                continue

            # parametersはoptionalなので、デフォルト値を空リストとする
            parameters = obj.get('parameters', [])

            if obj['trigger'] == 'command':
                speech_scripts.append_command_script(
                    obj['command'], obj['texts'], parameters)

            if obj['trigger'] =='stage':
                speech_scripts.append_stage_script(
                    obj['stage'], obj['texts'], parameters)

    return speech_scripts
