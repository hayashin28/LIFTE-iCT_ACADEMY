# step08_collide_x.py
"""
Step08: 横方向の当たり判定を追加するステップ

★ねらい
- Step07 の「左右移動」に、「壁にぶつかったら止まる」処理を足す
- 土管やレンガを「当たり判定ありのオブジェクト（solid）」として扱う方法を学ぶ
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
    """画像ファイル候補の中から、最初に見つかったものを返します。"""
    for p in candidates:
        if p.is_file():
            return str(p)
    raise FileNotFoundError("必要な画像が足りません。assets/img を確認してください。")


class Hero(Image):
    """
    横移動＋左右反転ができる主人公クラス。
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


class StageWithCollideX(Widget):
    """
    横方向の当たり判定付きステージ。

    - 主人公が土管やレンガにぶつかったら、それ以上は進めないようにします。
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

        # 土管（当たり判定あり）
        self.pipe = Image(
            source=dokan_path,
            size=(64, 96),
            pos=(550, 0),
            size_hint=(None, None),
        )
        self.add_widget(self.pipe)

        # レンガ（当たり判定あり）
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

    # キー入力

    def on_key_down(self, window, key, scancode, codepoint, modifiers):
        if key == 276:
            self.key_left = True
        elif key == 275:
            self.key_right = True
        return True

    def on_key_up(self, window, key, scancode):
        if key == 276:
            self.key_left = False
        elif key == 275:
            self.key_right = False
        return True

    # 更新

    def update(self, dt: float):
        """
        横方向の移動 → 当たり判定 の順で処理します。
        """
        hero = self.hero
        solids = [self.pipe] + self.bricks  # 壁として扱うオブジェクトたち

        vx = 0.0
        if self.key_left:
            vx -= hero.speed
            hero.face_left()
        if self.key_right:
            vx += hero.speed
            hero.face_right()

        # 1フレーム分の移動を試してみる
        old_x = hero.x
        new_x = old_x + vx * dt

        # まずは画面端チェック
        new_x = max(0, min(new_x, Window.width - hero.width))
        hero.x = new_x

        # 壁(solids) との衝突チェック
        for solid in solids:
            if hero.collide_widget(solid):
                # 右方向に動いていた場合: 壁の左側で止める
                if vx > 0 and hero.right > solid.x:
                    hero.right = solid.x
                # 左方向に動いていた場合: 壁の右側で止める
                elif vx < 0 and hero.x < solid.right:
                    hero.x = solid.right
        # 縦方向はまだ固定のまま（重力は次のステップで）


class Step08CollideXApp(App):
    """Step08 用アプリ本体"""

    def build(self):
        Window.size = (960, 540)
        self.title = "Pipe & Jump 10 Lessons - Step08 Collide X"
        return StageWithCollideX()


if __name__ == "__main__":
    Step08CollideXApp().run()
