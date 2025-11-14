# step01_bg.py
"""
Step01: 背景だけを表示するステップ

★ねらい
- 「Kivy のアプリ」がどう動くのか、いちばん小さい例で体験する
- 画像ファイル(bg.png / bg.jpg)を画面いっぱいに表示する
"""

from pathlib import Path  # ファイルやフォルダの場所を扱う標準ライブラリです

from kivy.app import App          # Kivy アプリの土台になるクラス
from kivy.uix.widget import Widget  # 画面に置ける「なにもない箱」のようなもの
from kivy.uix.image import Image    # 画像を表示するための部品
from kivy.core.window import Window  # ウィンドウの大きさなどを扱うもの


# ------------------------------------------------------------
# 画像ファイルが入っているフォルダへの「道」をつくる
# ------------------------------------------------------------

# この Python ファイル(step01_bg.py)が置かれているフォルダ (retro-mario/) を基準にします
BASE_DIR = Path(__file__).resolve().parent

# retro_mario/assets/img フォルダまでのパスを組み立てます
ASSETS_DIR = BASE_DIR / "retro_mario" / "assets"
IMG_DIR = ASSETS_DIR / "img"


def first_existing(*candidates: Path) -> str:
    """
    いくつか候補を受け取って、
    「最初に見つかったファイル」のパスを文字列で返す関数。

    例:
        first_existing(IMG_DIR / "bg.png", IMG_DIR / "bg.jpg")

    どれも存在しない場合は、わざとエラーを出して気づけるようにします。
    """
    for p in candidates:
        if p.is_file():  # 実際にそのファイルが存在するか？
            return str(p)

    # ここに来るということは、候補がぜんぶ見つからなかったということ
    raise FileNotFoundError(
        "背景画像が見つかりません。retro_mario/assets/img に "
        "bg.png または bg.jpg を置いてください。"
    )


# ------------------------------------------------------------
# 画面に背景を1枚だけ出すウィジェット
# ------------------------------------------------------------

class BackgroundOnly(Widget):
    """
    背景画像を1枚だけ表示する「画面」のクラス。

    ここでは、ゲームの細かい処理はなにもせず、
    「画像を敷き詰める」ことだけを担当させています。
    """

    def __init__(self, **kwargs):
        # 親クラス(Widget)の初期化をちゃんと呼びます
        super().__init__(**kwargs)

        # bg.png か bg.jpg のどちらかを探します
        bg_path = first_existing(IMG_DIR / "bg.png", IMG_DIR / "bg.jpg")

        # 画像を置く部品(Image)を作ります
        bg = Image(
            source=bg_path,   # さがしてきた画像ファイル
            allow_stretch=True,  # 画像を引き伸ばしてもよい
            keep_ratio=False,    # 縦横比(アスペクト比)は気にしない
            size_hint=(1, 1),    # 親(画面全体)に対して「全体いっぱい」
            pos=(0, 0),          # 左下から表示
        )

        # このウィジェット(画面)の上に、背景画像を乗せます
        self.add_widget(bg)


# ------------------------------------------------------------
# アプリ本体
# ------------------------------------------------------------

class Step01BackgroundApp(App):
    """
    Kivy アプリ本体のクラス。

    - build() の戻り値が「最初に表示する画面」になります。
    """

    def build(self):
        # ウィンドウの初期サイズを決めておきます（フルHD の半分くらい）
        Window.size = (960, 540)

        # ウィンドウに表示するタイトル(左上などに出る名前)
        self.title = "Pipe & Jump 10 Lessons - Step01 Background"

        # さきほど作った画面(BackgroundOnly)を、最初の画面として返します
        return BackgroundOnly()


# このファイルを「直接」実行したときだけ、アプリを起動します。
# （ほかのファイルから import したときには動かないようにするおまじない）
if __name__ == "__main__":
    Step01BackgroundApp().run()
