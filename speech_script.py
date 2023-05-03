from functools import reduce
from numbers import Number
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
        return self.apply_parameters_to_texts(parameters)

    def apply_parameters_to_texts(self, parameters):
        return list(map(lambda x: x.format(*parameters), self._texts))

    def _extract_parameters(self, referee_msg):
        # parametersにセットされた属性をreferee_msgから抽出する
        parameters = []
        for param_str in self._parameters:
            param_str_list = param_str.split('.')
            param = reduce(lambda obj, attr: getattr(obj, attr),
                           param_str_list, referee_msg)

            param = self._negative_value_to_text(param)
            parameters.append(param)
        return parameters

    def _negative_value_to_text(self, value):
        # -123という数値が正しく音声再生できなかったので、マイナス123のように変換する
        if not isinstance(value, Number):
            return value

        if value < 0:
            return 'マイナス' + str(abs(value))
        return value

class SpeechScripts:
    def __init__(self):
        self._command_scripts = {}
        self._stage_scripts = {}
        self._team_info_scripts = {}

    def append_command_script(self, command, texts, parameters):
        self._command_scripts[command] = SpeechScript(texts, parameters)

    def append_stage_script(self, stage, texts, parameters):
        self._stage_scripts[stage] = SpeechScript(texts, parameters)

    def append_team_info_script(self, team_info, texts, parameters):
        self._team_info_scripts[team_info] = SpeechScript(texts, parameters)

    def has_script_of_command(self, command):
        return command in self._command_scripts.keys()

    def has_script_of_stage(self, stage):
        return stage in self._stage_scripts.keys()

    def has_script_of_team_info(self, team_info):
        return team_info in self._team_info_scripts.keys()

    def get_script_of_command(self, command, referee_msg):
        return self._command_scripts[command].get_texts(referee_msg)

    def get_script_of_stage(self, stage, referee_msg):
        return self._stage_scripts[stage].get_texts(referee_msg)

    def get_script_of_team_info(self, team_info, team="blue", value=""):
        parameters = [team, value]
        return self._team_info_scripts[team_info].apply_parameters_to_texts(parameters)

    def get_team_info_script_triggers(self):
        return self._team_info_scripts.keys()


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

            if obj['trigger'] =='team_info':
                speech_scripts.append_team_info_script(
                    obj['team_info'], obj['texts'], parameters)

    return speech_scripts
