# step03_dokan.py
"""
Step03: 土管を追加するステップ

★ねらい
- 背景 + 雲 にくわえて、「地面のもの（土管）」を追加する
- 土管もただの画像であり、「置き方は雲と同じ」という感覚をつかむ
"""

from pathlib import Path

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.core.window import Window


BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "retro_mario" / "assets"
IMG_DIR = ASSETS_DIR / "img"


def first_existing(*candidates: Path) -> str:
    """画像ファイル候補の中から、最初に見つかったものを返します。"""
    for p in candidates:
        if p.is_file():
            return str(p)
    raise FileNotFoundError(
        "必要な画像(bg.png/bg.jpg/cloud.png/dokan.png)が足りません。retro_mario/assets/img を確認してください。"
    )


class BackgroundCloudsPipe(Widget):
    """
    背景 + 雲 + 土管 を表示する画面。
    ここでは、まだ当たり判定はつけません（飾りとして出すだけ）。
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        bg_path = first_existing(IMG_DIR / "bg.png", IMG_DIR / "bg.jpg")
        cloud_path = first_existing(IMG_DIR / "cloud.png")
        dokan_path = first_existing(IMG_DIR / "dokan.png")

        # 背景
        bg = Image(
            source=bg_path,
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1),
            pos=(0, 0),
        )
        self.add_widget(bg)

        # 雲（Step02 と同じ）
        for pos in [(80, 360), (420, 420), (720, 360)]:
            cloud = Image(
                source=cloud_path,
                size=(256, 96),
                pos=pos,
                size_hint=(None, None),
            )
            self.add_widget(cloud)

        # 土管を1つ置く
        # ここでは「画面の左から 550px の位置」に配置しています。
        pipe = Image(
            source=dokan_path,
            size=(64, 96),      # 推奨サイズ 64x96
            pos=(550, 0),       # 地面(下端)にくっつけるイメージ
            size_hint=(None, None),
        )
        self.add_widget(pipe)


class Step03DokanApp(App):
    """Step03 用アプリ本体"""

    def build(self):
        Window.size = (960, 540)
        self.title = "Pipe & Jump 10 Lessons - Step03 Pipe"
        return BackgroundCloudsPipe()


if __name__ == "__main__":
    Step03DokanApp().run()
