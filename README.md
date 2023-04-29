# RoboCup SSL Voice Referee

RoboCup SSLのレフェリー信号に合わせて音声を再生するPythonソフトウェアです

## Requirements

- Ubuntu (x86 64 arch)
- Docker
  - [voicevox/voicevoix_engine](https://hub.docker.com/r/voicevox/voicevox_engine)

## Instalation

```sh
$ sudo apt install python3-pip python3-protobuf
$ pip install simpleaudio
```

## Usage

Launch the VOICEVOX engine:

```sh
# Launch CPU engine
$ docker run --rm -it -p '127.0.0.1:50021:50021' voicevox/voicevox_engine:cpu-ubuntu20.04-latest

# or GPU engine
$ docker run --rm --gpus all -p '127.0.0.1:50021:50021' voicevox/voicevox_engine:nvidia-ubuntu20.04-latest
```

then bellow command:

```sh
$ cd path/to/robocup-ssl-voice-referee
$ python3 main.py
```

## References:

- RoboCup SSL Offical Protocol: https://github.com/RoboCup-SSL/ssl-game-controller/tree/master/proto

## LICENSE

Apache License Version 2.0

