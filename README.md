# VRChat IO

**Work in progress.**

VRChat IO is a library for input and output of VRChat data.

## Installation

```bash
pip install "git+https://github.com/Geson-anko/vrchat-io.git@main"
```

Note: Linux is future support.

### VRChat

1. Steamからインストール

   <https://store.steampowered.com/app/438100/VRChat/>

   [Linux Userはこのサイトを参考にしてください](https://ask.vrchat.com/t/guide-to-vrc-on-linux/15934)

2. VRChatを起動する

   Note: Steamの起動オプションに `-screen-width <pixel> -screen-height <pixel>`を設定すると常に同じサイズで出力されるので便利です。
   起動オプション参考: <https://docs.vrchat.com/docs/launch-options>

3. OSCを有効化する: <https://docs.vrchat.com/docs/osc-overview>

   Note: 起動オプションで `inPort:outIP:outPort`を設定できます。

### OBS (For video capture)

VRChatの映像をキャプチャし、Pythonから取得するためにOBSの仮想カメラを用います。

1. Download and Install OBS: <https://obsproject.com>

2. 仮想カメラをインストール

   - Windows:

     1. obs-virtualcamをインストール: <https://github.com/Avasam/obs-virtual-cam/releases>
     2. `ツール -> VirtualCam`から仮想カメラを開始。

   - Linux (仮想カメラが無い場合):

     1. `v4l2loopback`をインストール: <https://linuxgamecast.com/2021/07/obs-linux-basics-virtual-webcam/>
     2. OBSを再起動して *仮想カメラを開始*

3. VRChatのウィンドウをキャプチャする。

## Features

(Implement below things in the future.)

- [ ] Video Capture: 統一されたAPIを定義し、VRChatのプレイ映像をキャプチャします。内部ライブラリの処理を隠ぺいします。
- [ ] Audio Capture: 統一されたAPIを定義し、VRChatの音声をキャプチャします。
- [ ] OSC Input
- [ ] OSC Output
- [ ] etc...
