# -*- coding: utf-8 -*-
"""
game/obstacle.py – 障害物（レーン上の矩形）
"""
from dataclasses import dataclass
from typing import Tuple
from src import config

@dataclass
class Obstacle:
    lane: int
    x: float
    y: float
    w: float = config.OBSTACLE_W
    h: float = config.OBSTACLE_H
    alive: bool = True

    def rect(self) -> Tuple[float, float, float, float]:
        half_w = self.w * 0.5
        half_h = self.h * 0.5
        return (self.x - half_w, self.y - half_h, self.x + half_w, self.y + half_h)

    def update(self, dt: float, speed: float):
        """下方向へスクロール"""
        self.y -= speed * dt
        if self.y < -self.h:  # 画面外で消去
            self.alive = False
