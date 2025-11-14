# step10_goomba_spawn.py
"""
Step10: クリボー出現＋往復パトロールのステップ

★ねらい
- Step09 の主人公(横移動＋ジャンプ＋当たり判定)はそのまま
- 新たに「敵キャラ(クリボー)」を追加し、横に行ったり来たりさせる
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


# 主人公クラス（Step09 と同じ）

class Hero(Image):
    """横移動＋ジャンプができる主人公クラス。"""

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


# 敵キャラ（クリボー）クラス

class Goomba(Image):
    """
    クリボーもどきの敵キャラ。

    - 一定速度で左右に歩きます。
    - direction が 1 のとき右、-1 のとき左に進みます。
    """

    speed = NumericProperty(100.0)
    direction = NumericProperty(-1.0)

    def __init__(self, **kwargs):
        goomba_path = first_existing(IMG_DIR / "goomba.png")
        super().__init__(
            source=goomba_path,
            allow_stretch=True,
            keep_ratio=True,
            **kwargs,
        )
        self.size = (48, 48)
        self.size_hint = (None, None)


class StageWithGoomba(Widget):
    """
    主人公＋地形＋クリボーが登場するステージ。

    - 主人公: Step09 と同じ挙動（横移動＋ジャンプ＋当たり判定）
    - クリボー: Pipe 周辺を左右にパトロール
    """

    GRAVITY = -1800.0

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

        # 地形
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

        # クリボー
        self.goomba = Goomba()
        # 土管の右側あたりからスタート
        self.goomba.pos = (self.pipe.right + 40, 96)
        self.add_widget(self.goomba)

        # 入力状態
        self.key_left = False
        self.key_right = False

        Window.bind(on_key_down=self.on_key_down, on_key_up=self.on_key_up)
        Clock.schedule_interval(self.update, 1 / 60.0)

    # 入力

    def on_key_down(self, window, key, scancode, codepoint, modifiers):
        if key == 276:
            self.key_left = True
        elif key == 275:
            self.key_right = True
        elif key in (273, 32):
            self.try_jump()
        return True

    def on_key_up(self, window, key, scancode):
        if key == 276:
            self.key_left = False
        elif key == 275:
            self.key_right = False
        return True

    def try_jump(self):
        if self.hero.on_ground:
            self.hero.vy = self.hero.jump_speed
            self.hero.on_ground = False

    # 更新

    def update(self, dt: float):
        self.update_hero(dt)
        self.update_goomba(dt)

    def update_hero(self, dt: float):
        """主人公の移動・ジャンプ・当たり判定を処理します。"""
        hero = self.hero
        solids = [self.pipe] + self.bricks

        # 横方向
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

        for solid in solids:
            if hero.collide_widget(solid):
                if vx > 0 and hero.right > solid.x:
                    hero.right = solid.x
                elif vx < 0 and hero.x < solid.right:
                    hero.x = solid.right

        # 縦方向（重力＋当たり判定）
        hero.vy += self.GRAVITY * dt
        prev_y = hero.y
        hero.y += hero.vy * dt
        hero.on_ground = False

        # 地面
        if hero.y < 0:
            hero.y = 0
            hero.vy = 0
            hero.on_ground = True

        for solid in solids:
            if hero.collide_widget(solid):
                # 上から着地
                if prev_y >= solid.top and hero.y < solid.top:
                    hero.y = solid.top
                    hero.vy = 0
                    hero.on_ground = True
                # 下から頭をぶつけた
                elif prev_y + hero.height <= solid.y and hero.top > solid.y:
                    hero.top = solid.y
                    hero.vy = 0

    def update_goomba(self, dt: float):
        """
        クリボーの単純な往復パトロール処理。
        - 一定速度で左右に歩く
        - 画面端や地形にぶつかったら方向転換する
        """
        g = self.goomba
        solids = [self.pipe] + self.bricks

        old_x = g.x
        new_x = old_x + g.speed * g.direction * dt
        g.x = new_x

        # 画面端チェック
        if g.x < 0:
            g.x = 0
            g.direction *= -1
        elif g.right > Window.width:
            g.right = Window.width
            g.direction *= -1

        # 地形との当たり判定
        for solid in solids:
            if g.collide_widget(solid):
                if g.direction > 0 and g.right > solid.x:
                    g.right = solid.x
                    g.direction *= -1
                elif g.direction < 0 and g.x < solid.right:
                    g.x = solid.right
                    g.direction *= -1


class Step10GoombaSpawnApp(App):
    """Step10 用アプリ本体"""

    def build(self):
        Window.size = (960, 540)
        self.title = "Pipe & Jump 10 Lessons - Step10 Goomba Patrol"
        return StageWithGoomba()


if __name__ == "__main__":
    Step10GoombaSpawnApp().run()
