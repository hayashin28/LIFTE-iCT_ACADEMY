# -*- coding: utf-8 -*-
# Day2: ステージ構成の強化（パララックス背景／障害3種／フェアスポーン／難度曲線／デバッグ）
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.properties import ListProperty
from kivy.uix.label import Label

from ..config import P
from ..ui.hud import build_hud
from ..ui.parallax import ParallaxLayer
from ..game.player import Player
from ..game.obstacle import Obj
from ..game.spawner import SpawnState

# ---- ユーティリティ ----
def clamp(v, lo, hi): return lo if v < lo else hi if v > hi else v
def aabb(ax, ay, aw, ah, bx, by, bw, bh):
    # 四角形どうしの重なり判定（AABB）。4つの不等式のAND。
    return (ax < bx + bw and ax + aw > bx and ay < by + bh and ay + ah > by)

# ---- dp変換済みの座標 ----
GROUND_Y    = dp(P.GROUND_Y_PX)
LOW_JUMP_H  = dp(P.JUMP_TIER_PX)

class GroundLine(Widget):
    color = ListProperty([0.6,0.6,0.9,1])

class PlayScene:
    """
    なぜ: Day1の骨格に、背景の奥行き・理不尽でない出現・多様な障害を追加して「ゲーム性」を授業で扱う。
    前提: 60FPS相当で update()。Pool使い回し。dp()で解像度差を吸収。
    """
    def __init__(self, engine=None):
        self.engine = engine
        self.root = None
        self.lbl = None
        self.lbl_dbg = None
        self.time = 0.0
        self.speed = P.BASE_SPEED
        self.score = 0
        self.energy = 100
        self.game_over = False
        self.debug = P.DEBUG_ON_START

    def on_enter(self, root_widget, engine):
        from kivy.clock import Clock
        self.engine = engine
        self.root = root_widget
        self.container = FloatLayout(size=(Window.width, Window.height))
        self.root.add_widget(self.container)

        # 0) 背景（パララックス）
        self._build_parallax()

        # 1) HUD
        self.lbl = build_hud()
        self.container.add_widget(self.lbl)
        # デバッグラベル（F1で切替）
        self.lbl_dbg = Label(text="", size_hint=(1,None), height=dp(20), pos=(0, dp(10)))

        # 2) 地面
        self.ground = GroundLine(size=(Window.width, dp(6)))
        self.ground.pos = (0, GROUND_Y - dp(6))
        self.container.add_widget(self.ground)

        # 3) プレイヤー
        self.player = Player(size=(dp(52), dp(52)))
        self.player.color = [0.2,0.9,1,1]
        self.player.pos = (dp(80), GROUND_Y)
        self.container.add_widget(self.player)

        # 4) オブジェクトプール（8体：連結が来ても枯渇しない）
        self.objects = []
        for _ in range(8):
            o = Obj(size=(dp(42), dp(42)))
            self._style_obj(o, "ob_low")  # とりあえず低障害風
            # 右の外に置いておく
            o.pos = (Window.width + dp(999), GROUND_Y)
            self.objects.append(o)
            self.container.add_widget(o)

        # 5) スポーン状態（フェア規則）
        self.spawn = SpawnState(P, ground_y_px=P.GROUND_Y_PX, low_jump_h_px=P.JUMP_TIER_PX)
        # 最初の並びを確定
        for o in self.objects:
            self._recycle_one(o, first=True)

        # 6) 入力
        Window.bind(on_key_down=self._on_key_down)

        # 7) 更新ループ
        self._ev = Clock.schedule_interval(self.update, 1/60)

    def on_exit(self):
        from kivy.clock import Clock
        try:
            Window.unbind(on_key_down=self._on_key_down)
            if self._ev: self._ev.cancel()
        except Exception:
            pass

    # ---------- 背景 ----------
    def _build_parallax(self):
        self.bg_layers = []
        total_h = sum(P.BG_BAND_HEIGHTS_PX)
        y_top = Window.height
        # 上から下へ帯を配置
        for i in range(P.BG_BANDS):
            h_px = P.BG_BAND_HEIGHTS_PX[i]
            color = P.BG_COLORS[i]
            ratio = P.BG_SPEED_RATIOS[i]
            band = ParallaxLayer(band_h_px=h_px, color=color, size=(Window.width, dp(h_px)))
            # 帯のy。上から詰める（空を上に、地形風を下に）
            y_top -= dp(h_px)
            band.pos = (0, y_top)
            self.container.add_widget(band)
            self.bg_layers.append((ratio, band))

    # ---------- 入力 ----------
    def _on_key_down(self, _w, key, *_a):
        # F1: デバッグ切替
        if key == 282:  # KivyのF1（環境差はあり）
            self.debug = not self.debug
            if self.debug and self.lbl_dbg.parent is None:
                self.container.add_widget(self.lbl_dbg)
            elif not self.debug and self.lbl_dbg.parent is not None:
                self.container.remove_widget(self.lbl_dbg)
            return True
        # GameOver中: Enter/Spaceで再開
        if self.game_over and key in (13, 32):
            self._restart(); return True
        # 通常: Up/Spaceでジャンプ
        if key in (273, 32):
            self._jump(); return True
        return False

    # ---------- 本体更新 ----------
    def update(self, dt):
        if self.game_over: 
            return

        # 背景パララックス（画面の動きを先に）
        for ratio, band in self.bg_layers:
            band.tick(dt, speed_px_s=self.speed * ratio)

        # 時間・速度段階
        self.time += dt
        self._update_speed()

        # 物理
        self._apply_physics(dt)

        # スクロール＆再配置
        self._scroll_and_recycle(dt)

        # 当たり判定
        self._handle_collisions()

        # スコア/体力
        self._tick_score_energy(dt)

        # HUD / Debug
        self._refresh_ui()

        # ゲームオーバー判定
        self._check_game_over()

    # ---------- ジャンプ ----------
    def _jump(self):
        if self.player.on_ground and not self.game_over:
            self.player.vy = P.JUMP_V
            self.player.on_ground = False

    # ---------- 物理 ----------
    def _apply_physics(self, dt):
        self.player.vy -= P.GRAVITY * dt
        px, py = self.player.pos
        py += self.player.vy * dt
        if py <= GROUND_Y:
            py = GROUND_Y
            self.player.vy = 0.0
            self.player.on_ground = True
        self.player.pos = (px, py)

    # ---------- スクロール＆再配置 ----------
    def _scroll_and_recycle(self, dt):
        for o in self.objects:
            # 種別により微妙に速度差（コインはやや遅い）
            vx = self.speed if o.kind.startswith("ob") else self.speed * 0.9
            x, y = o.pos
            x -= vx * dt
            # 画面左を出たら右へ再配置
            if x < -o.width:
                self._recycle_one(o)
            else:
                o.pos = (x, y)

    def _recycle_one(self, o, first=False):
        # スポーン状態から次配置を取得
        item = self.spawn.next_item(speed=self.speed)
        kind = item["kind"]
        x_px = item["x"]; y_px = item["y"]
        w_px, h_px = item["size"]

        # サイズ・色・種別
        self._style_obj(o, kind, w_px, h_px)
        # 位置（dp変換）
        o.pos = (dp(x_px), dp(y_px))

        # 初期は密集を避けるため、next_x を更に先へ
        if first:
            self.spawn.next_x += 0  # ここでは既に初期分散済み

    def _style_obj(self, o, kind: str, w_px=None, h_px=None):
        # 色分け：障害=赤系／コイン=緑
        if kind == "coin":
            o.color = [0.35, 1.0, 0.35, 1]
        elif kind == "ob_high":
            o.color = [1.0, 0.55, 0.40, 1]
        elif kind == "ob_train":
            o.color = [1.0, 0.40, 0.55, 1]
        else:  # ob_low
            o.color = [1.0, 0.35, 0.40, 1]
        o.kind = kind
        # サイズ（px→dp）
        if w_px and h_px:
            o.size = (dp(w_px), dp(h_px))

    # ---------- 当たり判定 ----------
    def _handle_collisions(self):
        for o in self.objects:
            if aabb(self.player.x, self.player.y, self.player.width, self.player.height,
                    o.x, o.y, o.width, o.height):
                if o.kind.startswith("ob"):
                    self.energy -= 22
                else:
                    self.energy = clamp(self.energy + 14, 0, 100)
                    self.score += 12
                self._recycle_one(o)  # ぶつかったら即再配置

    # ---------- 難度（速度段階） ----------
    def _update_speed(self):
        tiers = int(self.time // P.SPEED_INTERVAL)
        self.speed = P.BASE_SPEED + tiers * P.SPEED_STEP

    # ---------- スコア/体力 ----------
    def _tick_score_energy(self, dt):
        self.score += int(P.SCORE_RATE * dt)
        self.energy = max(0, self.energy - P.ENERGY_DECAY * dt)

    # ---------- UI ----------
    def _refresh_ui(self):
        self.lbl.text = f"Score: {self.score}   Energy: {int(self.energy)}"
        if self.debug:
            self.lbl_dbg.text = (f"[dbg] t={self.time:5.1f}s  speed={self.speed:.1f}  "
                                f"next_x≈{self.spawn.next_x:.0f}  last={self.spawn.last_kind}")
            if self.lbl_dbg.parent is None:
                self.container.add_widget(self.lbl_dbg)

    # ---------- ゲームオーバー ----------
    def _check_game_over(self):
        if self.energy <= 0 and not self.game_over:
            self.game_over = True
            self.lbl.text = f"[ GAME OVER ] Score: {self.score}  (Enter/Space/Touch to Restart)"

    # ---------- 再開 ----------
    def _restart(self):
        self.time = 0.0
        self.speed = P.BASE_SPEED
        self.score = 0
        self.energy = 100
        self.game_over = False
        self.player.pos = (dp(80), GROUND_Y)
        self.player.vy = 0.0
        self.player.on_ground = True
        # スポーン状態を初期化し直す
        self.spawn = SpawnState(P, ground_y_px=P.GROUND_Y_PX, low_jump_h_px=P.JUMP_TIER_PX)
        for o in self.objects:
            self._recycle_one(o, first=True)
        return True
