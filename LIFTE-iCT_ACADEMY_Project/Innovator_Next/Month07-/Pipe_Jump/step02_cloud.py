# step02_cloud.py
"""
Step02: 背景に「雲」を足すステップ

★ねらい
- 背景の上に、画像をいくつか重ねて表示する方法を知る
- 同じ画像(cloud.png)を、場所を変えて何回も使う練習
"""

from pathlib import Path

from kivymd.app import MDApp as App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.core.window import Window


# パスの作り方は Step01 と同じです
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"
IMG_DIR = ASSETS_DIR / "img"


def first_existing(*candidates: Path) -> str:
    """Step01 と同じヘルパー関数。最初に見つかったファイルのパスを返します。"""
    for p in candidates:
        if p.is_file():
            return str(p)
    raise FileNotFoundError(
        "必要な画像ファイルが見つかりません。assets/img を確認してください。"
    )


class BackgroundWithClouds(Widget):
    """
    背景＋雲を表示する画面。

    - 背景: 画面いっぱいに敷き詰め
    - 雲  : cloud.png を複数コピーして配置
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # 背景画像と雲画像のパスを探します
        bg_path = first_existing(IMG_DIR / "bg.png", IMG_DIR / "bg.jpg")
        cloud_path = first_existing(IMG_DIR / "cloud.png")

        # まずは背景を一番下に敷きます
        bg = Image(
            source=bg_path,
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1),
            pos=(0, 0),
        )
        self.add_widget(bg)

        # 雲をいくつか置いてみます。
        # size_hint を None にして、ピクセルサイズを直接指定しています。
        cloud_positions = [
            (80, 360),
            (420, 420),
            (720, 360),
        ]
        for x, y in cloud_positions:
            cloud = Image(
                source=cloud_path,
                size=(256, 96),      # たとえば 512x128 の画像を半分のサイズで出すイメージ
                pos=(x, y),
                size_hint=(None, None),
            )
            self.add_widget(cloud)


class Step02CloudApp(App):
    """Step02 用アプリ本体"""

    def build(self):
        Window.size = (960, 540)
        self.title = "Pipe & Jump 10 Lessons - Step02 Clouds"
        return BackgroundWithClouds()


if __name__ == "__main__":
    Step02CloudApp().run()
