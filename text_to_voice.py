import json
from pathlib import Path
import requests
import simpleaudio
import urllib.parse

class TextToVoice():
    def __init__(self, addr="localhost", port=50021, no_voice=False):
        self._playing_obj = None
        self._server_url = "http://" + addr + ":" + str(port)
        self._no_voice = no_voice  # Trueでデバッグ用の音声再生なしモード

    def _get_query(self, text, speaker_id):
        success = True
        query = None

        url = self._server_url + "/audio_query?speaker=" \
            + str(speaker_id) \
            + "&text=" + urllib.parse.quote(text)
        try:
            response = requests.post(url)
            response.raise_for_status()
            query = response.json()
        except requests.exceptions.RequestException as e:
            print("    Error: can not get query because:{}".format(e))
            success = False

        return success, query

    def _generate_wav_file(self, file_path, query, speaker_id):
        success = True

        url = self._server_url + "/synthesis?speaker=" + str(speaker_id)
        wav_path = Path(file_path)
        try:
            response = requests.post(url, json=query)
            response.raise_for_status()
            wav_path.write_bytes(response.content)
        except requests.exceptions.RequestException as e:
            print("    Error: can not get wav data because:{}".format(e))
            success = False
        
        return success

    def play(self, text="", speaker_id=1, speed_scale=1.2, volume_scale=1.0):
        if self._no_voice:
            print("No Voice Mode: Play:{}".format(text))
            return True

        success, query = self._get_query(text, speaker_id)
        if not success:
            return False

        query['speedScale'] = speed_scale
        query['volumeScale'] = volume_scale

        file_path = 'output.wav'
        if not self._generate_wav_file(file_path, query, speaker_id):
            return False

        wav_obj = simpleaudio.WaveObject.from_wave_file(file_path)
        self._playing_obj = wav_obj.play()
        return True

    def stop(self):
        if self._playing_obj:
            self._playing_obj.stop()
    
    def is_playing(self):
        if self._playing_obj:
            return self._playing_obj.is_playing()
        return False
