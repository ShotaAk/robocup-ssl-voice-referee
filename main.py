import requests
import urllib.parse
import simpleaudio
from pathlib import Path
import yaml
import argparse
import socket
import ssl_gc_referee_message_pb2
import time

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

    speech_scripts = load_speech_scripts()

    prev_command_count = -1
    while True:
        rcv_data, addr = sock.recvfrom(1024)
        referee_msg = ssl_gc_referee_message_pb2.Referee()
        referee_msg.ParseFromString(rcv_data)

        # コマンドが更新されたらテキストを読み上げる
        if prev_command_count != referee_msg.command_counter:
            prev_command_count = referee_msg.command_counter
            command = referee_msg.command

            if command in speech_scripts.keys():
                for text in speech_scripts[command].get_texts():
                    text_to_voice(text)
                    time.sleep(1)  # 休みなく読み上げることを防ぐ
                    
            else:
                print('コマンド:{}に対応した原稿がありません'.format(command))

    sock.close()
