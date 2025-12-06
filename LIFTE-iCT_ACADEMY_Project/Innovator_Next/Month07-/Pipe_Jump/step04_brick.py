# step04_brick.py
"""
Step04: レンガブロックを追加するステップ

★ねらい
- 同じレンガ画像を横に並べて「足場」を表現する
- 「ブロックもやっぱり画像を並べているだけ」という感覚をつかむ
"""

from pathlib import Path

from kivymd.app import MDApp as App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.core.window import Window


BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"
IMG_DIR = ASSETS_DIR / "img"


def first_existing(*candidates: Path) -> str:
    """画像ファイル候補の中から、最初に見つかったものを返します。"""
    for p in candidates:
        if p.is_file():
            return str(p)
    raise FileNotFoundError(
        "必要な画像(bg.png/bg.jpg/cloud.png/dokan.png/brick_block.png)が足りません。assets/img を確認してください。"
    )


class BackgroundCloudsPipeBricks(Widget):
    """
    背景 + 雲 + 土管 + レンガ を描画する画面。
    当たり判定はまだなく、まずは「見た目の地形」を作る段階です。
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        bg_path = first_existing(IMG_DIR / "bg.png", IMG_DIR / "bg.jpg")
        cloud_path = first_existing(IMG_DIR / "cloud.png")
        dokan_path = first_existing(IMG_DIR / "dokan.png")
        brick_path = first_existing(IMG_DIR / "brick_block.png")

        # 背景
        bg = Image(
            source=bg_path,
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1),
            pos=(0, 0),
        )
        self.add_widget(bg)

        # 雲
        for pos in [(80, 360), (420, 420), (720, 360)]:
            cloud = Image(
                source=cloud_path,
                size=(256, 96),
                pos=pos,
                size_hint=(None, None),
            )
            self.add_widget(cloud)

        # 土管
        pipe = Image(
            source=dokan_path,
            size=(64, 96),
            pos=(550, 0),
            size_hint=(None, None),
        )
        self.add_widget(pipe)

        # レンガブロックを横一列に並べる
        # 「for ループで少しずつ x 座標をずらす」というパターンを学ぶ目的もあります。
        brick_y = 200
        brick_w, brick_h = 128, 32
        for i in range(4):
            x = 300 + i * brick_w
            brick = Image(
                source=brick_path,
                size=(brick_w, brick_h),
                pos=(x, brick_y),
                size_hint=(None, None),
            )
            self.add_widget(brick)


class Step04BrickApp(App):
    """Step04 用アプリ本体"""

    def build(self):
        Window.size = (960, 540)
        self.title = "Pipe & Jump 10 Lessons - Step04 Bricks"
        return BackgroundCloudsPipeBricks()


if __name__ == "__main__":
    Step04BrickApp().run()
