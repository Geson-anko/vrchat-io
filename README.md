# VRChat IO

VRChat IO is a library for inputting data into and getting data from VRChat. (For AI, Machine Learnings.)

VRChat IOは、VRChatにデータを入力したり、VRChatから取得したりするためのライブラリです。

## Installation

### Supported Platforms

- Windows 10, 11
- Linux (Ubuntu, Debian, Arch Linux, etc...)

### Command

```bash
pip install "git+https://github.com/Geson-anko/vrchat-io.git@main"
```

or clone this repository and run following command in the directory.  (Installing from source.)

```bash
# ./vrchat-io
pip install -e .
```

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

### Video Capture

```py
cam = VideoCapture(...)
frame = cam.read()
```

- OpenCVVideoCapture

  `cv2.VideoCapture`の簡易ラッパーです。`read`メソッドを用いて画像を読み出します。
  取得する画像の`width`, `height`は指定できますが、などはあくまでも期待される値であり、実際に得られる画像とは異なる場合があることに注意してください。

画像を任意のアスペクト比、解像度で必ず取得したい場合は`vrchat_io.vrchat_io.vision.wrappers`内部の[RatioCropWrapper](/vrchat_io/vision/wrappers/ratio_crop_wrapper.py)や[ResizeWrapper](/vrchat_io/vision/wrappers/resize_wrapper.py)を用いてください。

[DEMOファイルはこちらです。](/demos/opencv_video_capture_demo.py)

### Controller

- OSC Input Controller

  `python-osc`の`SimpleUDPClient`のラッパークラスです。OSCで送信し操作できる項目に関しては[`vrchat-io.controller.osc`の`Axes`や`Buttons`の属性として列挙されているのでそれを用いてください。](/vrchat_io/controller/osc/input_controller.py)

  [InputControllerに関するDemoファイルはこちらです。](/demos/osc_input_controller_demo.py)

  このInputControllerにも`Wrapper`クラスが用意されており、インターフェイスをラップすることで目的に応じて使いやすくすることができます。[DEMOファイルはこちらです。](/demos/interactive_osc_controller_demo.py)

### Future Features

(Implement below things in the future.)

- [ ] Video Capture: 統一されたAPIを定義し、VRChatのプレイ映像をキャプチャします。内部ライブラリの処理を隠ぺいします。
- [ ] Audio Capture: 統一されたAPIを定義し、VRChatの音声をキャプチャします。
- [x] OSC Input
- [ ] OSC Output
- [ ] etc...
