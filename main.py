import requests
import urllib.parse
import simpleaudio
from pathlib import Path
import yaml
import argparse
import socket

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

class SpeechScript:
    def __init__(self, command, stage, texts):
        self._target_command = command
        self._target_stage = stage
        self._texts = texts

    def get_target_command(self):
        return self._target_command

    def get_target_stage(self):
        return self._target_stage

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
            script = SpeechScript(obj['command'], obj['stage'], obj['texts'])

            speech_script_dict[script.get_target_command()] = script

    return speech_script_dict

def main():
    pass



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--addr',
        type=str,
        default='224.5.23.1', help='Set IP address to receive referee command.',
        required=False,
        )
    parser.add_argument('--port',
        type=int,
        default=10003, help='Set IP port to receive referee command.',
        required=False,
        )
    args = parser.parse_args()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Avoid error 'Address already in use'.
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Construct a membership_request
    membership_request = socket.inet_aton(args.addr) + socket.inet_aton('0.0.0.0')
    # Send add membership request to socket
    sock.setsockopt(socket.IPPROTO_IP, 
        socket.IP_ADD_MEMBERSHIP, membership_request)
    # Bind the socket to an interfaces
    sock.bind((args.addr, args.port))
    # # Set non-blocking receiving mode

    while True:
        rcv_data, addr = sock.recvfrom(1024)
        print("receive data : [{}]  from {}".format(rcv_data,addr))

    sock.close()

    main()
