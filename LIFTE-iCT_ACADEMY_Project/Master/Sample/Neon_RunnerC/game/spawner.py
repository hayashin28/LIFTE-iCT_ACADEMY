# -*- coding: utf-8 -*-
"""
game/spawner.py – 障害物生成（周期＋ランダム）
"""
import random
from typing import List
from src import config
from src.game.obstacle import Obstacle

class Spawner:
    def __init__(self):
        self.timer = 0.0
        self.next_interval = self._next_interval()

    def _next_interval(self) -> float:
        """次の生成間隔を決める（ベース ± ランダム、下限あり）"""
        jitter = random.uniform(-config.SPAWN_RANDOM_JITTER, config.SPAWN_RANDOM_JITTER)
        iv = max(config.SPAWN_MIN_INTERVAL, config.SPAWN_BASE_INTERVAL + jitter)
        return iv

    def update(self, dt: float, obstacles: List[Obstacle], speed: float):
        self.timer += dt
        if self.timer >= self.next_interval:
            self.timer = 0.0
            self.next_interval = self._next_interval()

            # 1～2 個をまとめて出すことも（揺らぎ）
            count = 1 if random.random() < 0.7 else 2
            lanes = list(range(config.LANES))
            random.shuffle(lanes)
            for i in range(count):
                lane = lanes[i % config.LANES]
                x = config.lane_x(lane)
                y = config.HEIGHT + config.OBSTACLE_H  # 画面の上から出現
                obstacles.append(Obstacle(lane=lane, x=x, y=y))
