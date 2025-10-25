# -*- coding: utf-8 -*-
"""
RPG_Steel_MasterD — TEACHER設定（Day1/Day2共通）
- 生徒版と同値。授業中に可変パラメータの根拠を示せるよう集約。
"""
WIDTH, HEIGHT = 960, 540
FPS = 60
TILE_SIZE = 32
MAP_CSV = "assets/maps/steel_map01.csv"
TILESET_IMAGE = "assets/maps/steel_tileset.png"
TILESET_COLUMNS = 8

# 挙動
PLAYER_SPEED = 2.2
RUN_MULTIPLIER = 1.7
PLAYER_ACCEL = 0.55
PLAYER_FRICTION = 0.72

# 色/UI
BG = (18, 20, 24)
BLUE = (90, 170, 255)
GREEN = (80, 200, 120)
YELLOW = (245, 210, 80)
WHITE = (240, 240, 240)
RED = (230, 90, 90)
FONT_SIZE = 18
