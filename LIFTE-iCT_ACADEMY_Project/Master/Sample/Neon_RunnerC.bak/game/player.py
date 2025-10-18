# -*- coding: utf-8 -*-
"""
game/player.py – プレイヤー（レーン移動 + ジャンプ）

設計方針：
- プレイヤーの x はレーン中心にスナップ（0..LANES-1）。
- y は連続値。地面（GROUND_Y）を床として重力/ジャンプを適用。
- 入力は on_key_down で「離散操作」（レーン移動）と「瞬時操作」（ジャンプ）を処理。
- 当たり判定は AABB：矩形 (x-w/2,y-h/2)-(x+w/2,y+h/2) を使用。
"""
from dataclasses import dataclass
from typing import Tuple
from time import monotonic

from .. import config

@dataclass
class Player:
    lane: int = 1                     # 中央レーンから開始（0..LANES-1）
    x: float = config.lane_x(1)
    y: float = config.PLAYER_GROUND_Y
    vy: float = 0.0
    w: float = config.PLAYER_W
    h: float = config.PLAYER_H
    hp: int = config.START_HP
    inv_until: float = 0.0            # 無敵の終了時刻（monotonic 秒）

    def rect(self) -> Tuple[float, float, float, float]:
        """AABB 用の (left, bottom, right, top)"""
        half_w = self.w * 0.5
        half_h = self.h * 0.5
        return (self.x - half_w, self.y - half_h, self.x + half_w, self.y + half_h)

    # --- 操作 ---
    def move_left(self):
        if self.lane > 0:
            self.lane -= 1
            self.x = config.lane_x(self.lane)

    def move_right(self):
        if self.lane < config.LANES - 1:
            self.lane += 1
            self.x = config.lane_x(self.lane)

    def try_jump(self):
        # 地上に近い場合のみジャンプを許可
        if self.y <= config.PLAYER_GROUND_Y + 1.0:
            self.vy = config.JUMP_VELOCITY

    # --- 更新 ---
    def update(self, dt: float):
        """重力と床判定を適用"""
        self.vy -= config.GRAVITY * dt
        self.y += self.vy * dt
        # 床でクリップ
        if self.y < config.PLAYER_GROUND_Y:
            self.y = config.PLAYER_GROUND_Y
            self.vy = 0.0

    # --- ダメージ処理 ---
    def can_damage(self, now_s: float) -> bool:
        return now_s >= self.inv_until and self.hp > 0

    def on_hit(self, now_s: float):
        """衝突時の HP 減少と無敵時間付与"""
        if self.can_damage(now_s):
            self.hp -= 1
            self.inv_until = now_s + config.INVULN_TIME
