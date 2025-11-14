# step09_jump_basic.py
"""
Step09: 重力＋ジャンプ＋縦の当たり判定を追加するステップ

★ねらい
- 重力(下向きの加速度)とジャンプ(上向きの初速)を導入する
- 地面(y=0)や土管・レンガに対し、「上から着地」「下から頭をぶつける」を判定する
"""

from pathlib import Path

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import BooleanProperty, NumericProperty


BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "retro_mario" / "assets"
IMG_DIR = ASSETS_DIR / "img"


def first_existing(*candidates: Path) -> str:
    """必要な画像ファイル候補から、最初に見つかったものを返します。"""
    for p in candidates:
        if p.is_file():
            return str(p)
    raise FileNotFoundError("必要な画像が足りません。retro_mario/assets/img を確認してください。")


class Hero(Image):
    """
    横移動 + ジャンプができる主人公クラス。

    - speed      : 左右移動の速さ（ピクセル/秒）
    - vy         : 上下方向の速度（プラス: 上向き / マイナス: 下向き）
    - jump_speed : ジャンプ開始時の上向き初速
    - on_ground  : 地面やブロックの上に乗っているかどうか
    """

    speed = NumericProperty(220.0)
    vy = NumericProperty(0.0)
    jump_speed = NumericProperty(900.0)
    on_ground = BooleanProperty(False)
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
        self._flipped = False

    def face_left(self):
        """キャラを左向きにする"""
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


class StageWithJump(Widget):
    """
    横＋縦方向の当たり判定＋ジャンプ付きステージ。

    - GRAVITY: 下向きの加速度（負の値）
    """

    GRAVITY = -1800.0  # 下向き加速度（数値を大きくすると「ずんっ」と落ちる）

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

        # 地形（当たり判定対象）
        self.pipe = Image(
            source=dokan_path,
            size=(64, 96),
            pos=(550, 0),
            size_hint=(None, None),
        )
        self.add_widget(self.pipe)

        self.bricks = []
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
            self.bricks.append(brick)
            self.add_widget(brick)

        # 主人公
        self.hero = Hero()
        self.hero.pos = (120, 96)
        self.add_widget(self.hero)

        # 入力状態
        self.key_left = False
        self.key_right = False

        Window.bind(on_key_down=self.on_key_down, on_key_up=self.on_key_up)
        Clock.schedule_interval(self.update, 1 / 60.0)

    # 入力

    def on_key_down(self, window, key, scancode, codepoint, modifiers):
        if key == 276:  # 左矢印
            self.key_left = True
        elif key == 275:  # 右矢印
            self.key_right = True
        elif key in (273, 32):  # 上矢印 or Space でジャンプ
            self.try_jump()
        return True

    def on_key_up(self, window, key, scancode):
        if key == 276:
            self.key_left = False
        elif key == 275:
            self.key_right = False
        return True

    def try_jump(self):
        """
        ジャンプキーが押されたときに呼ばれます。

        地面(on_ground=True)にいるときだけ、ジャンプ開始速度を与えます。
        """
        if self.hero.on_ground:
            self.hero.vy = self.hero.jump_speed
            self.hero.on_ground = False

    # 更新

    def update(self, dt: float):
        hero = self.hero
        solids = [self.pipe] + self.bricks

        # ---- 横方向の処理 ----
        vx = 0.0
        if self.key_left:
            vx -= hero.speed
            hero.face_left()
        if self.key_right:
            vx += hero.speed
            hero.face_right()

        old_x = hero.x
        new_x = old_x + vx * dt
        new_x = max(0, min(new_x, Window.width - hero.width))
        hero.x = new_x

        # 横当たり判定
        for solid in solids:
            if hero.collide_widget(solid):
                if vx > 0 and hero.right > solid.x:
                    hero.right = solid.x
                elif vx < 0 and hero.x < solid.right:
                    hero.x = solid.right

        # ---- 縦方向の処理（重力＋当たり判定） ----

        # 重力を速度に反映
        hero.vy += self.GRAVITY * dt

        prev_y = hero.y  # 1フレーム前の高さを記録
        hero.y += hero.vy * dt
        hero.on_ground = False  # いったん「空中」と仮定

        # 地面(y=0)との当たり判定
        if hero.y < 0:
            hero.y = 0
            hero.vy = 0
            hero.on_ground = True

        # ブロックや土管との縦方向当たり
        for solid in solids:
            if hero.collide_widget(solid):
                # 上から着地したパターン
                if prev_y >= solid.top and hero.y < solid.top:
                    hero.y = solid.top
                    hero.vy = 0
                    hero.on_ground = True
                # 下から頭をぶつけたパターン
                elif prev_y + hero.height <= solid.y and hero.top > solid.y:
                    hero.top = solid.y
                    hero.vy = 0


class Step09JumpBasicApp(App):
    """Step09 用アプリ本体"""

    def build(self):
        Window.size = (960, 540)
        self.title = "Pipe & Jump 10 Lessons - Step09 Jump Basic"
        return StageWithJump()


if __name__ == "__main__":
    Step09JumpBasicApp().run()
