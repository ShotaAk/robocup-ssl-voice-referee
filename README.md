# RoboCup SSL Voice Referee

RoboCup SSLのレフェリー信号に合わせて音声を再生するPythonソフトウェアです

## Requirements

- Ubuntu (x86 64 arch)
- VOICEVOX

## Instalation

### VOICEVOX

Please see https://voicevox.hiroshiba.jp/product/zundamon/ for details.

```sh
# Install packages required for VOICEVOX
$ sudo apt install p7zip fuse

# Download VOICEVOX installer for linux.
$ wget https://voicevox.hiroshiba.jp/static/b4e3b7fe1eceb58d763ad439d9c35ec7/linuxInstallCpu.sh
$ chmod +x linuxInstallCpu.sh
$ ./linuxInstallCpu.sh

VOICEVOX has been installed under ~/.voicevox directory.

# Example: launch VOICEVOX app
$ ~/.voicevox/VOICEVOX.AppImage
```

### Python modules

```sh
$ sudo apt install python3-pip python3-protobuf
$ pip install simpleaudio
```

## Usage

Launch the VOICEVOX app:

```sh
$ ~/.voicevox/VOICEVOX.AppImage
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

