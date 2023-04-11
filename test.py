import requests
import urllib.parse
import simpleaudio
from pathlib import Path

def text_to_voice(text="テストです", speaker_id=1):

    # クエリ取得
    # TODO: request失敗時の例外処理を追加する
    url = "http://localhost:50021/audio_query?speaker=" \
        + str(speaker_id) \
        + "&text=" + urllib.parse.quote(text)

    response = requests.post(url)
    if response.status_code != 200:
        return -1
    query = response.json()

    # wav取得
    # TODO: request失敗時の例外処理を追加する
    url = "http://localhost:50021/synthesis?speaker=" + str(speaker_id)
    response = requests.post(url, json=query)
    if response.status_code != 200:
        return -1
    
    file_name = 'output.wav'
    wav_path = Path(file_name)
    wav_path.write_bytes(response.content)

    # 再生
    wav_obj = simpleaudio.WaveObject.from_wave_file(file_name)
    play_obj = wav_obj.play()
    play_obj.wait_done()


if __name__ == "__main__":
    main()
