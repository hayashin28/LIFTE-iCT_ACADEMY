# step07_move_lr.py
"""
Step07: 主人公を ←→ キーで動かすステップ

★ねらい
- キーボード入力(矢印キー)でキャラを左右に動かす
- 左右を向いたときに、キャラの画像も左右反転させる
- まだ地形との当たり判定はない（すり抜けOK）
"""

from pathlib import Path

from kivymd.app import MDApp as App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import BooleanProperty, NumericProperty


BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"
IMG_DIR = ASSETS_DIR / "img"


def first_existing(*candidates: Path) -> str:
    """必要な画像ファイル候補から、最初に見つかったものを返します。"""
    for p in candidates:
        if p.is_file():
            return str(p)
    raise FileNotFoundError("必要な画像が足りません。assets/img を確認してください。")


class Hero(Image):
    """
    左右に歩ける主人公クラス。

    - speed: 1秒あたり何ピクセル動くか
    - facing_left: 左を向いているかどうか
    """

    speed = NumericProperty(220.0)
    facing_left = BooleanProperty(False)

    def __init__(self, **kwargs):
        hero_path = first_existing(IMG_DIR / "hero_idle.png", IMG_DIR / "mario.png")
        super().__init__(
            source=hero_path,
            allow_stretch=True,
            keep_ratio=True,
            **kwargs,
        )
        self.size = (64, 64)
        self.size_hint = (None, None)
        self._flipped = False  # テクスチャを左右反転させているかどうか

    def face_left(self):
        """キャラを左向きにする（テクスチャ左右反転）"""
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


class StageWithMovingHero(Widget):
    """
    背景 + 地形 + 動く主人公 を表示・更新する画面。

    ポイント:
    - Window.bind(on_key_down, on_key_up) でキー状態を記録
    - Clock.schedule_interval(update, 1/60) で毎フレーム update() を呼ぶ
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

        # 主人公
        self.hero = Hero()
        self.hero.pos = (120, 96)
        self.add_widget(self.hero)

        # キーの状態（押されている間 True になります）
        self.key_left = False
        self.key_right = False

        # キー入力イベントを受け取るように登録します
        Window.bind(on_key_down=self.on_key_down, on_key_up=self.on_key_up)

        # 1/60秒ごとに update() を呼んで、主人公を動かします
        Clock.schedule_interval(self.update, 1 / 60.0)

    # ------------------------
    # キー入力の処理
    # ------------------------

    def on_key_down(self, window, key, scancode, codepoint, modifiers):
        """
        キーが押されたときに呼ばれる関数。

        key には「キーの番号」が入ってきます。
        ここでは、矢印キーの番号だけを使っています。
        ・左矢印: 276
        ・右矢印: 275
        """
        if key == 276:  # 左
            self.key_left = True
        elif key == 275:  # 右
            self.key_right = True
        return True  # イベントを「ここで処理済みです」と伝える

    def on_key_up(self, window, key, scancode):
        """キーが離されたときに呼ばれる関数。"""
        if key == 276:
            self.key_left = False
        elif key == 275:
            self.key_right = False
        return True

    # ------------------------
    # 毎フレーム呼ばれる update
    # ------------------------

    def update(self, dt: float):
        """
        1/60秒ごとに呼ばれます。

        dt には「前回からの経過時間(秒)」が渡されるので、
        speed(ピクセル/秒) × dt(秒) で移動量を計算します。
        """
        vx = 0.0

        # 入力に応じて左右速度を決める
        if self.key_left:
            vx -= self.hero.speed
            self.hero.face_left()
        if self.key_right:
            vx += self.hero.speed
            self.hero.face_right()

        # 1フレーム分の移動量を計算
        new_x = self.hero.x + vx * dt

        # 画面の左右端で止める（外にはみ出さないようにする）
        new_x = max(0, min(new_x, Window.width - self.hero.width))

        # 計算した位置を反映
        self.hero.x = new_x
        # y はこのステップでは固定のままです（重力はまだ）


class Step07MoveLRApp(App):
    """Step07 用アプリ本体"""

    def build(self):
        Window.size = (960, 540)
        self.title = "Pipe & Jump 10 Lessons - Step07 Move Left/Right"
        return StageWithMovingHero()


if __name__ == "__main__":
    Step07MoveLRApp().run()
