# RoboCup SSL Voice Referee

RoboCup SSLのレフェリー信号に合わせて音声を再生するPythonソフトウェアです

## Requirements

- Ubuntu (x86 64 arch)
- Docker
  - [voicevox/voicevoix_engine](https://hub.docker.com/r/voicevox/voicevox_engine)

## Instalation

Install dependencies:

```sh
sudo apt install python3-pip python3-protobuf
pip install simpleaudio
```

Install `voiceref` directory:

```sh
pip install -v https://github.com/ShotaAk/robocup-ssl-voice-referee
```

(Optional) Install `voiceref` locally:

```sh
git clone https://github.com/ShotaAk/robocup-ssl-voice-referee
cd robocup-ssl-voice-referee
pip install -v .
```

## Usage

Launch the VOICEVOX engine:

```sh
# Launch CPU engine
$ docker run --rm -it -p '127.0.0.1:50021:50021' voicevox/voicevox_engine:cpu-ubuntu20.04-latest

# or GPU engine
$ docker run --rm --gpus all -p '127.0.0.1:50021:50021' voicevox/voicevox_engine:nvidia-ubuntu20.04-latest
```

then execute bellow commands:

```sh
python3 -m voiceref.main
```


### Options

Execute bellow command:

```sh
python3 -m voiceref.main --help
```

```sh
usage: main.py [-h] [--referee_addr REFEREE_ADDR]
               [--referee_port REFEREE_PORT] [--voicevox_addr VOICEVOX_ADDR]
               [--voicevox_port VOICEVOX_PORT] [--no_voice]

options:
  -h, --help            show this help message and exit
  --referee_addr REFEREE_ADDR
                        Set IP address to receive referee command.
  --referee_port REFEREE_PORT
                        Set IP port to receive referee command.
  --voicevox_addr VOICEVOX_ADDR
                        Set IP address for VOICEVOX server.
  --voicevox_port VOICEVOX_PORT
                        Set IP port for VOICEVOX server.
  --no_voice            Run this script without VOICEVOX.
```

## References

- RoboCup SSL Offical Protocol: https://github.com/RoboCup-SSL/ssl-game-controller/tree/master/proto

## LICENSE

Apache License Version 2.0
