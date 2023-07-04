# VRChat IO

**Work in progress.**

VRChat IO is a library for sending and getting VRChat data. (For AI, Machine Learnings.)

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

### Video Capture

- OpenCVVideoCapture
  `cv2.VideoCapture`の簡易ラッパーです。解像度、フレームレート、BGR2RGBの変換など、基本的な事を実装します。

```py
from vrchat_io.vision import OpenCVVideoCapture
import cv2

cam = OpenCVVideoCapture(
   camera = cv2.VideoCapture(2), # Device index depends on your pc.
   width = 1920,
   height = 1080,
   fps = 30,
)

frame = cam.read(bgr2rgb=True) # Convert to rgb image.
```

### Input Controller

`python-osc`の`SimpleUDPClient`のラッパークラスです。

```py
from vrchat_io.osc import InputController, Axes, Buttons
from pythonosc.udp_client import SimpleUDPClient
import time

ctrlr = InputController(
   SimpleUDPClient("127.0.0.1", 9000)
)

ctrlr.command(Axes.Vertical, 0.5)
time.sleep(1.0)
ctrlr.command(Axes.Vertical, 0.0)
```

通常OSCで命令を送信した後は、必ずリセットの命令を出す必要があります。指定した時間の後にそうするためには`command_and_reset`メソッドを用います。Backgroundスレッドで実行する場合は`command_and_reset_background`を用います。

```py
from vrchat_io.osc import InputController, Axes, Buttons
from pythonosc.udp_client import SimpleUDPClient

ctrlr = InputController(
   SimpleUDPClient("localhost", 9000)
)

# It moves forward for one second and then stops.

ctrlr.command_and_reset(
   Buttons.MoveForward, # command address
   1, # Input value
   0, # Reset value
   duration = 1.0, # The reset value(s) is sent after duration [seconds]
)
```

### Future Features

(Implement below things in the future.)

- [ ] Video Capture: 統一されたAPIを定義し、VRChatのプレイ映像をキャプチャします。内部ライブラリの処理を隠ぺいします。
- [ ] Audio Capture: 統一されたAPIを定義し、VRChatの音声をキャプチャします。
- [x] OSC Input
- [ ] OSC Output
- [ ] etc...
