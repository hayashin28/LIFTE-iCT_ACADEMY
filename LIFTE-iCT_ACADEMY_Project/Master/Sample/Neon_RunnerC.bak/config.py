# -*- coding: utf-8 -*-
"""
config.py – ゲーム全体の設定を集中管理（魔法値の排除）

なぜ→ 調整を容易にし、授業中のデバッグを速くするため。
前提→ Kivy で矩形描画。レーン制の縦スクロール無限ランナー。
入出力→ なし（値を import して参照）
副作用→ なし
例外→ 画面サイズやレーン数を変更する場合は lane_x() の確認を。
"""
from math import floor

# 画面
WIDTH  = 480
HEIGHT = 720
FPS    = 60

# レーン
LANES = 3                         # 3 レーン（0,1,2）
LANE_MARGIN = 40                  # 左右の余白（px）

# プレイヤー
PLAYER_W = 56
PLAYER_H = 56
PLAYER_GROUND_Y = 120             # 地面の Y（px）
GRAVITY = 1800.0                  # 重力（px/sec^2）
JUMP_VELOCITY = 700.0             # ジャンプ初速度（px/sec）
INVULN_TIME = 1.0                 # 無敵時間（秒）
START_HP = 3

# スクロール/速度
BASE_SPEED = 220.0                # 下方向スクロール速度の基準（px/sec）
ACCEL_PER_SEC = 18.0              # 秒あたりの加速（px/sec^2）
MAX_SPEED = 540.0                 # 上限

# 生成（Spawner）
SPAWN_BASE_INTERVAL = 1.1         # 基本間隔（秒）
SPAWN_RANDOM_JITTER = 0.5         # ±ランダム（秒）
SPAWN_MIN_INTERVAL  = 0.45        # 下限（速すぎ防止）

# 障害物
OBSTACLE_W = 56
OBSTACLE_H = 56

# HUD 表示フラグ
HUD_DEFAULT_VISIBLE = True

def lane_x(index: int) -> float:
    """レーン中心 X を返す。index は 0..LANES-1"""
    usable = WIDTH - LANE_MARGIN*2
    step = usable / (LANES - 1) if LANES > 1 else 0
    return LANE_MARGIN + step * index
