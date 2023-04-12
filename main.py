#!/usr/bin/env python3

import argparse
import time

from text_to_voice import text_to_voice
from speech_script import load_speech_scripts
from referee_receiver import RefereeReceiver


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

    print("Start Robocup SSL Voice Referee")
    print("    Usage: Ctrl-C to exit\n")

    print("Check VOICEVOX connection...")
    if text_to_voice(""):
        print("    OK\n")
    else:
        print("Exit.")
        exit(1)

    ref_receiver = RefereeReceiver(args.addr, args.port)
    speech_scripts = load_speech_scripts()

    print("Waiting for referee command...")
    prev_command_count = -1
    try:
        while True:
            referee_msg = ref_receiver.get_referee_message()

            # コマンドが更新されたらテキストを読み上げる
            if prev_command_count != referee_msg.command_counter:
                prev_command_count = referee_msg.command_counter
                command = referee_msg.command

                if command in speech_scripts.keys():
                    for text in speech_scripts[command].get_texts():
                        print("Play text: {}".format(text))
                        text_to_voice(text)
                        time.sleep(1)  # 休みなく読み上げることを防ぐ
                        
                else:
                    print('コマンド:{}に対応した原稿がありません'.format(command))
    except KeyboardInterrupt:
        pass

    ref_receiver.close()
    print("\nExit.")
    exit(0)
