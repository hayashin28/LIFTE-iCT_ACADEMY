# -*- coding: utf-8 -*-
"""
scenes/play.py – プレイ画面（レーン移動/ジャンプ、生成、衝突、HUD、ポーズ）

厚いコメント方針：
- なぜ：Day1 の学習効果最大化のため、実装意図とバグりやすい論点を文中で指示。
- 入出力：キーボード入力→内部状態更新→矩形描画→HUD。
- 例外：依存を増やさず Kivy 標準のみ。画像を使わず矩形で高速化。
"""
from time import monotonic
from typing import List, Tuple

from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle, InstructionGroup
from kivy.core.window import Window
from kivy.clock import Clock

from src import config
from src.ui.hud import HUD
from src.game.player import Player
from src.game.obstacle import Obstacle
from src.game.spawner import Spawner

def aabb_overlap(a: Tuple[float,float,float,float], b: Tuple[float,float,float,float]) -> bool:
    """AABB の交差判定。a=(l,b,r,t)"""
    return not (a[2] < b[0] or a[0] > b[2] or a[3] < b[1] or a[1] > b[3])

class PlayField(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = (config.WIDTH, config.HEIGHT)

        # ゲーム状態
        self.player = Player(lane=1, x=config.lane_x(1), y=config.PLAYER_GROUND_Y)
        self.obstacles: List[Obstacle] = []
        self.spawner = Spawner()

        # ランタイム値
        self.t = 0.0                 # 経過時間（sec）
        self.speed = config.BASE_SPEED
        self.score = 0.0
        self.paused = False
        self.hud_visible = config.HUD_DEFAULT_VISIBLE

        # 入力
        self._kb = None
        Clock.schedule_once(self._bind_kb, 0)

        # HUD
        self.hud = HUD()
        self.add_widget(self.hud)

        # ループ開始
        self._tick = Clock.schedule_interval(self.update, 1.0 / config.FPS)

    # --- 入力 ---
    def _bind_kb(self, *_):
        self._kb = Window.request_keyboard(self._kb_closed, self)
        if self._kb:
            self._kb.bind(on_key_down=self._on_key_down)

    def _kb_closed(self, *_):
        if self._kb:
            self._kb.unbind(on_key_down=self._on_key_down)
            self._kb = None

    def _on_key_down(self, keyboard, keycode, text, modifiers):
        _, s = keycode
        s = s.lower()
        if s in ("left", "a"):
            self.player.move_left()
            return True
        if s in ("right", "d"):
            self.player.move_right()
            return True
        if s in ("spacebar", "space"):
            self.player.try_jump()
            return True
        if s == "p":
            self.paused = not self.paused
            return True
        if s == "h":
            self.hud_visible = not self.hud_visible
            self.hud.visible = self.hud_visible
            return True
        return False

    # --- 更新ループ ---
    def update(self, dt: float):
        if self.paused:
            self._draw()
            self._update_hud()
            return

        # 経過時間と速度（加速して上限で打ち止め）
        self.t += dt
        self.speed = min(config.MAX_SPEED, config.BASE_SPEED + config.ACCEL_PER_SEC * self.t)

        # スコア：生存時間×速度の簡易指標
        self.score += self.speed * dt * 0.1

        # プレイヤー更新
        self.player.update(dt)

        # 生成と更新
        self.spawner.update(dt, self.obstacles, self.speed)
        for o in self.obstacles:
            o.update(dt, self.speed)
        self.obstacles = [o for o in self.obstacles if o.alive]

        # 衝突判定（無敵時間考慮）
        now_s = monotonic()
        if self.player.can_damage(now_s):
            prect = self.player.rect()
            for o in self.obstacles:
                if aabb_overlap(prect, o.rect()):
                    self.player.on_hit(now_s)
                    # 当たった障害物は消す（多段ヒット防止）
                    o.alive = False
                    break

        # 描画と HUD
        self._draw()
        self._update_hud()

    # --- 描画 ---
    def _draw(self):
        self.canvas.clear()
        with self.canvas:
            # 背景
            Color(0.05, 0.06, 0.10, 1.0)
            Rectangle(pos=(0, 0), size=self.size)

            # レーン床（薄いライン）
            Color(0.18, 0.20, 0.30, 1.0)
            for i in range(config.LANES):
                x = config.lane_x(i) - 2
                Rectangle(pos=(x, 0), size=(4, config.HEIGHT))

            # 地面
            Color(0.12, 0.14, 0.22, 1.0)
            Rectangle(pos=(0, 0), size=(config.WIDTH, config.PLAYER_GROUND_Y - 8))

            # プレイヤー（無敵中は明滅）
            alpha = 1.0
            from time import monotonic
            if not self.player.can_damage(monotonic()):
                alpha = 0.4
            Color(0.90, 0.95, 1.0, alpha)
            Rectangle(
                pos=(self.player.x - self.player.w/2, self.player.y - self.player.h/2),
                size=(self.player.w, self.player.h)
            )

            # 障害物
            Color(0.95, 0.35, 0.45, 1.0)
            for o in self.obstacles:
                Rectangle(pos=(o.x - o.w/2, o.y - o.h/2), size=(o.w, o.h))

    def _update_hud(self):
        self.hud.set_info(dict(score=self.score, hp=self.player.hp, speed=self.speed, paused=self.paused))

class PlayScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(PlayField())
