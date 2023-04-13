import json
from pathlib import Path
import requests
import simpleaudio
import urllib.parse

def text_to_voice(text="テストです", speaker_id=1, speed_scale=1.2, volume_scale=1.0):
    # クエリ取得
    url = "http://localhost:50021/audio_query?speaker=" \
        + str(speaker_id) \
        + "&text=" + urllib.parse.quote(text)
    query = None
    try:
        response = requests.post(url)
        response.raise_for_status()
        query = response.json()
    except requests.exceptions.RequestException as e:
            print("    Error: can not get query because:{}".format(e))
            return False

    # クエリ加工
    query['speedScale'] = speed_scale
    query['volumeScale'] = volume_scale

    # wav取得
    url = "http://localhost:50021/synthesis?speaker=" + str(speaker_id)
    file_name = 'output.wav'
    wav_path = Path(file_name)
    try:
        response = requests.post(url, json=query)
        response.raise_for_status()
        wav_path.write_bytes(response.content)
    except requests.exceptions.RequestException as e:
            print("    Error: can not get wav data because:{}".format(e))
            return False

    # 再生
    wav_obj = simpleaudio.WaveObject.from_wave_file(file_name)
    play_obj = wav_obj.play()
    play_obj.wait_done()
    return True