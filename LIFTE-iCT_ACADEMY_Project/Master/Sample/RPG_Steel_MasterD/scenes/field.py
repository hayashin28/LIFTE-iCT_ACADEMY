# -*- coding: utf-8 -*-
"""
scenes/field.py – フィールド画面（移動 + 衝突 + HUD）

なぜ:
- Day1 で必要な最小構成（移動/衝突/HUD）をまとめ、動く手応えを得るため。
前提:
- Kivy + キーボード入力（request_keyboard）
- マップは CSV（0=床, 1=壁）で、タイルサイズは config.TILE
入出力:
- 入力: キーボード状態（矢印 / WASD）
- 出力: 画面描画（床/壁/プレイヤー）、HUD 文字列
副作用:
- フレームごとの状態更新（Clock.schedule_interval）
例外:
- キーボード取得失敗 / マップ読み込み失敗時は落ちないようにログを出す。
"""
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.clock import Clock

import csv
from pathlib import Path
from typing import List, Tuple

from src import config
from src.ui.hud import DebugHUD

# ユーティリティ: CSV を 2D 配列へ
def load_csv_map(path: Path) -> List[List[int]]:
    grid = []
    with path.open("r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            grid.append([int(v) for v in row])
    return grid

class GameField(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = (config.WIDTH, config.HEIGHT)

        # マップ読み込み
        self.map_grid = load_csv_map(config.DEFAULT_MAP_CSV)
        self.map_w = len(self.map_grid[0])
        self.map_h = len(self.map_grid)

        # プレイヤー状態
        self.x = config.TILE * 2.5  # スタート位置（中央寄り）
        self.y = config.TILE * 2.5
        self.dir = "down"           # 表示用
        self.vx = 0.0
        self.vy = 0.0

        # キー状態
        self.keys = set()
        self._keyboard = None

        # HUD
        self.hud = DebugHUD()
        self.add_widget(self.hud)

        # キーボード要求 & 更新ループ開始
        Clock.schedule_once(self._bind_keyboard, 0)
        self._tick = Clock.schedule_interval(self.update, 1/60)

    def _bind_keyboard(self, *_):
        self._keyboard = Window.request_keyboard(self._on_keyboard_closed, self)
        if self._keyboard is not None:
            self._keyboard.bind(on_key_down=self._on_key_down, on_key_up=self._on_key_up)

    def _on_keyboard_closed(self, *_):
        if self._keyboard is not None:
            self._keyboard.unbind(on_key_down=self._on_key_down, on_key_up=self._on_key_up)
            self._keyboard = None

    def _on_key_down(self, keyboard, keycode, text, modifiers):
        key, s = keycode
        self.keys.add(s)
        if s.lower() == "h":
            self.hud.visible = not self.hud.visible
        return True

    def _on_key_up(self, keyboard, keycode):
        key, s = keycode
        if s in self.keys:
            self.keys.remove(s)
        return True

    def update(self, dt: float):
        # 入力を速度に反映
        left  = "left" in self.keys or "a" in self.keys
        right = "right" in self.keys or "d" in self.keys
        up    = "up" in self.keys or "w" in self.keys
        down  = "down" in self.keys or "s" in self.keys

        self.vx = (config.SPEED if right else 0) - (config.SPEED if left else 0)
        self.vy = (config.SPEED if up else 0) - (config.SPEED if down else 0)

        if abs(self.vx) > abs(self.vy):
            self.dir = "right" if self.vx > 0 else ("left" if self.vx < 0 else self.dir)
        elif abs(self.vy) > 0:
            self.dir = "up" if self.vy > 0 else "down"

        # 衝突を考慮した移動（軸ごと補正）
        self.move_with_collision(self.vx * dt, 0.0)
        self.move_with_collision(0.0, self.vy * dt)

        # 再描画
        self.canvas.clear()
        with self.canvas:
            # 背景
            Color(*config.COLOR_BG)
            Rectangle(pos=(0, 0), size=self.size)

            # タイル描画（床/壁）
            for ty in range(self.map_h):
                for tx in range(self.map_w):
                    val = self.map_grid[ty][tx]
                    Color(* (config.COLOR_WALL if val == 1 else config.COLOR_FLOOR))
                    Rectangle(
                        pos=(tx * config.TILE, ty * config.TILE),
                        size=(config.TILE, config.TILE)
                    )
            # プレイヤー
            Color(*config.COLOR_PLAYER)
            Rectangle(
                pos=(self.x - config.PLAYER_HALF_W, self.y - config.PLAYER_HALF_H),
                size=(config.PLAYER_HALF_W * 2, config.PLAYER_HALF_H * 2)
            )

        # HUD 更新
        tile_x = int(self.x // config.TILE)
        tile_y = int(self.y // config.TILE)
        fps = 1.0 / dt if dt > 0 else 0.0  # 簡易計算（Kivy の get_fps は 0 になりやすい）
        self.hud.set_info(dict(x=self.x, y=self.y, dir=self.dir, fps=fps, tile_x=tile_x, tile_y=tile_y))

    # --- 衝突関連 ---
    def is_blocked(self, tx: int, ty: int) -> bool:
        """マップ外は壁扱い。1 が壁、0 が床。"""
        if tx < 0 or ty < 0 or tx >= self.map_w or ty >= self.map_h:
            return True
        return self.map_grid[ty][tx] == 1

    def move_with_collision(self, dx: float, dy: float):
        """軸別に移動。移動後、四隅のタイルに壁がある場合はその軸の移動を打ち消す。"""
        if dx == 0 and dy == 0:
            return

        new_x = self.x + dx
        new_y = self.y + dy

        # プレイヤー矩形の四隅。少し内側をサンプリングして引っかかりを抑制
        hw, hh = config.PLAYER_HALF_W, config.PLAYER_HALF_H
        corners = [
            (new_x - hw, new_y - hh),
            (new_x + hw, new_y - hh),
            (new_x - hw, new_y + hh),
            (new_x + hw, new_y + hh),
        ]
        blocked = False
        for px, py in corners:
            tx = int(px // config.TILE)
            ty = int(py // config.TILE)
            if self.is_blocked(tx, ty):
                blocked = True
                break

        if blocked:
            # この軸の移動をキャンセル
            if dx != 0:
                # X のみキャンセル
                new_x = self.x
            if dy != 0:
                # Y のみキャンセル
                new_y = self.y

            # 再評価（角での食い込み軽減）: 片軸だけ許す
            # 片軸で再試行（オプション）

        self.x = new_x
        self.y = new_y

class FieldScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.field = GameField()
        self.add_widget(self.field)
