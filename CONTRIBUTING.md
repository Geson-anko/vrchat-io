# How to become a contributor and submit your own code

ここにはこのリポジトリへのコントリビューション方法を記述します。

## Policy

- シンプルかつミニマムに。小さな機能を積み重ねよう
- 未来の自分と開発者を救うために、ドキュメントは丁寧に。
- Issueから始めよ！自分が作るものを書き出そう。

## Contributing A Patch

1. どのような修正・機能追加のパッチを制作するのか、issueに記述してください。
2. このリポジトリをフォークし、実装してテストコードを記述してください。テストはすべての関数、メソッドに対して網羅的に行われている必要があります。
3. あなたのコードが既存のコードスタイルとマッチしているか確認してください。
4. すべてのテストコードがパスし、フォーマッタがかけられていることを確認してください。
5. プルリクエストを送信してください。

## Setting Up Your Dev Environment

### Prerequisites

- [Git](https://git-scm.com/)

- [Make](https://www.gnu.org/software/make/)

- [Python 3.10](https://www.python.org/downloads/)

- [poetry](https://python-poetry.org/docs/#installation)

  NOTE: You can install poetry using `pip install poetry` or `pip3 install poetry` depending on your system.

### Installation

1. このリポジトリをクローンしてください。
2. `poetry install` で依存関係をインストールします。
3. `poetry shell` で仮想環境に入ります (conda環境ですでに仮想環境にいる場合は無視して次のステップに進んでください。)
4. `make test-full`ですべてのコードが正常に動作するか、確かめてください。
5. (Optional) [demos](/demos/)のコードを実行し、自身の環境で意図した通りの動作をすることを確認してください。

## Developing

開発する際の基本的な方針や手順を示します。

### Abstract Class

[全く新しい種類の情報を扱う際はabcの内部に抽象クラスを設定し、インターフェイスを策定してください。](/vrchat_io/abc/)

現在は`Controller`と`VideoCapture`クラスの抽象クラス、そしてその抽象ラッパークラスが用意されています。

### Vision

[画像入力処理（視覚）に関する機能を実装する場合はvisionディレクトリ下に作成してください。](/vrchat_io/vision/)

#### VideoCapture

抽象VideoCaptureクラスを継承して制作します。`read`メソッドで画像のnumpy配列を返すようにしてください。

またラッパークラスを作る際は`VideoCaptureWrapper`抽象クラスを継承し、`visions/wrappers`下に制作してください。画像に前処理を加える場合は`FrameWrapper`クラスを利用すると便利です。

### Controller

[VRChatへ操作情報を送る処理を実装します。`controller`ディレクトリに作成してください。](/vrchat_io/controller/)

抽象Controllerクラスを継承して制作します。 `command`メソッドでVRChatに操作を送るように実装してください。ラッパークラスは`wrappers`フォルダに作成してください。

`osc`のInputControllerといった、大本から異なるコントローラーを制作する場合は内部にフォルダを作ってそこに実装してください。
