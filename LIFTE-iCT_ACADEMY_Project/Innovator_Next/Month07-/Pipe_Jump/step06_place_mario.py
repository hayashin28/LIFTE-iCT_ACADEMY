# step06_place_mario.py
"""
Step06: 主人公（配管工キャラ）を配置するステップ

★ねらい
- 「主人公キャラ」をクラスとして定義する
- まだ動かさず、「画面に立たせる」ことだけに集中する
"""

from pathlib import Path

from kivymd.app import MDApp as App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.properties import BooleanProperty  # キャラの「向き」などを状態として持つために使います


BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"
IMG_DIR = ASSETS_DIR / "img"


def first_existing(*candidates: Path) -> str:
    """画像ファイル候補の中から、最初に見つかったものを返します。"""
    for p in candidates:
        if p.is_file():
            return str(p)
    raise FileNotFoundError(
        "必要な画像(bg, cloud, dokan, brick_block, hero_idle/mario)が足りません。assets/img を確認してください。"
    )


class Hero(Image):
    """
    主人公キャラ用のクラス。

    今は「立っているだけ」ですが、Step07 以降で
    ・左右移動
    ・ジャンプ
    などの機能を少しずつ足していきます。
    """

    facing_left = BooleanProperty(False)  # 左向きなら True, 右向きなら False

    def __init__(self, **kwargs):
        # 主人公に使う画像を選びます。
        # hero_idle.png があればそれを優先し、なければ mario.png を使います。
        hero_path = first_existing(IMG_DIR / "hero_idle.png", IMG_DIR / "mario.png")

        super().__init__(
            source=hero_path,
            allow_stretch=True,
            keep_ratio=True,
            **kwargs,
        )

        # キャラの表示サイズ（64x64 ピクセルくらい）
        self.size = (64, 64)
        self.size_hint = (None, None)

        # テクスチャを左右反転しているかどうかのフラグ
        # （Step07 で使いますが、ここではまだ出番はありません）
        self._flipped = False

    # 以下2つのメソッドは「左右反転」のためのものです（Step07 で使用）
    def face_left(self):
        """キャラを左向きにする（テクスチャを左右反転する）"""
        if self._flipped:
            return
        if not self.texture:
            return
        tex = self.texture
        tex.uvpos = (1, 0)
        tex.uvsize = (-1, 1)
        self.texture = tex
        self.canvas.ask_update()
        self._flipped = True
        self.facing_left = True

    def face_right(self):
        """キャラを右向きに戻す"""
        if not self._flipped:
            return
        if not self.texture:
            return
        tex = self.texture
        tex.uvpos = (0, 0)
        tex.uvsize = (1, 1)
        self.texture = tex
        self.canvas.ask_update()
        self._flipped = False
        self.facing_left = False


class StaticStageWithHero(Widget):
    """
    背景 + 雲 + 土管 + レンガ + 主人公（静止）を表示する画面。

    Step04 + Step05 のステージに、「立っているだけの主人公」を追加した形です。
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

        # レンガ
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

        # 主人公（まだ動かない）
        hero = Hero()
        # 地面から少し上(96)の位置に立たせてみます
        hero.pos = (120, 96)
        self.add_widget(hero)


class Step06PlaceMarioApp(App):
    """Step06 用アプリ本体"""

    def build(self):
        Window.size = (960, 540)
        self.title = "Pipe & Jump 10 Lessons - Step06 Place Hero"
        return StaticStageWithHero()


if __name__ == "__main__":
    Step06PlaceMarioApp().run()
