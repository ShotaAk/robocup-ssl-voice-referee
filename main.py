#!/usr/bin/env python3

import argparse
from queue import Queue
import threading
import time

from text_to_voice import TextToVoice 
from speech_script import load_speech_scripts
from referee_receiver import RefereeReceiver


def text_to_voice_thread(stop_event):
    global text_queue_has_reset
    while not stop_event.is_set():
        if text_queue.empty():
            continue

        if text_queue_has_reset:
            text_queue_has_reset = False
            text_to_voice.stop()

        if text_to_voice.is_playing():
            continue
        
        text = text_queue.get()
        print("Play: {}".format(text))
        text_to_voice.play(text)

def reset_text_queue():
    global text_queue_has_reset
    while not text_queue.empty():
        text_queue.get()
    text_queue_has_reset = True

def main(speech_scripts):
    prev_command_count = -1
    prev_stage = -1
    while True:
        referee_msg = ref_receiver.get_referee_message()

        # コマンドが更新されたらテキストを読み上げる
        if prev_command_count != referee_msg.command_counter:
            prev_command_count = referee_msg.command_counter
            command = referee_msg.command
            stage = referee_msg.stage
            print("Referee command: {}, stage: {}".format(command, stage))

            reset_text_queue()

            if prev_stage != stage:
                prev_stage = stage
                if speech_scripts.has_script_of_stage(stage):
                    for text in speech_scripts.get_script_of_stage(stage, referee_msg):
                        text_queue.put(text)

            if speech_scripts.has_script_of_command(command):
                for text in speech_scripts.get_script_of_command(command, referee_msg):
                    text_queue.put(text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--referee_addr',
        type=str,
        default='224.5.23.1', help='Set IP address to receive referee command.',
        required=False,
        )
    parser.add_argument('--referee_port',
        type=int,
        default=10003, help='Set IP port to receive referee command.',
        required=False,
        )
    parser.add_argument('--voicevox_addr',
        type=str,
        default='localhost', help='Set IP address for VOICEVOX server.',
        required=False,
        )
    parser.add_argument('--voicevox_port',
        type=int,
        default=50021, help='Set IP port for VOICEVOX server.',
        required=False,
        )
    parser.add_argument('--no_voice', action='store_true')
    args = parser.parse_args()

    ref_receiver = RefereeReceiver(args.referee_addr, args.referee_port)
    text_to_voice = TextToVoice(args.voicevox_addr, args.voicevox_port, args.no_voice)
    speech_scripts = load_speech_scripts()
    text_queue = Queue()
    text_queue_has_reset = False

    print("Start Robocup SSL Voice Referee")
    print("    Usage: Ctrl-C to exit\n")

    print("Check VOICEVOX connection...")
    print("    Server address: {}, port: {}".format(args.voicevox_addr, args.voicevox_port))
    if text_to_voice.play(""):
        print("    OK\n")
    else:
        print("Exit.")
        exit(1)

    stop_event = threading.Event()
    play_thread = threading.Thread(target=text_to_voice_thread, args=(stop_event,))
    play_thread.start()

    print("Waiting for referee command...")
    print("    Server address: {}, port: {}".format(args.referee_addr, args.referee_port))
    try:
        main(speech_scripts)
    except KeyboardInterrupt:
        stop_event.set()

    ref_receiver.close()
    play_thread.join()
    print("\nExit.")
    exit(0)
