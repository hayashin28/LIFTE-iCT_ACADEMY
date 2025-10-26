# -*- coding: utf-8 -*-
# Day1+Day2 共通の調整パラメータを集約
from dataclasses import dataclass

@dataclass(frozen=True)
class P:
    # --- 画面・地面 ---
    WINDOW_W: int = 560
    WINDOW_H: int = 720
    GROUND_Y_PX: int = 90   # dp() 変換は使用側（scenes）で行う

    # --- 物理（ジャンプ） ---
    GRAVITY: float = 1200.0
    JUMP_V: float  = 460.0

    # --- スピード（難度曲線） ---
    BASE_SPEED: float     = 200.0
    SPEED_STEP: float     = 30.0
    SPEED_INTERVAL: float = 10.0  # 10秒ごとに速く

    # --- スポーン（共通） ---
    COIN_RATE: float        = 0.30
    SPAWN_SPREAD_PX: int    = 240
    JUMP_TIER_PX: int       = 90

    # --- Day2: フェア・スポーン規則 ---
    MIN_GAP_PX: int         = 140   # 次の出現までの最小距離
    EXTRA_GAP_AFTER_HIGH: int = 40  # 高障害の直後は少し余裕
    TRAIN_SEGMENTS_MIN: int = 2     # 連結障害の台数
    TRAIN_SEGMENTS_MAX: int = 3
    TRAIN_SEGMENT_GAP_PX: int = 22  # 連結間の短いギャップ
    # 種別の重み（合計は任意）：低/高/連結（障害）／コイン
    WEIGHT_OB_LOW: float  = 0.50
    WEIGHT_OB_HIGH: float = 0.25
    WEIGHT_OB_TRAIN: float= 0.15
    WEIGHT_COIN: float    = 0.10

    # Day2: 障害サイズ（px相当）※ dp() 変換は使用側
    OB_LOW_W: int  = 42;  OB_LOW_H: int  = 42
    OB_HIGH_W: int = 42;  OB_HIGH_H: int = 72

    # Day2: パララックス
    BG_BANDS: int = 3
    BG_SPEED_RATIOS: tuple = (0.25, 0.5, 0.8)   # BASE_SPEED に対する倍率
    BG_BAND_HEIGHTS_PX: tuple = (140, 110, 80)  # 上から順
    BG_COLORS: tuple = (
        (0.10, 0.10, 0.18, 1.0),
        (0.16, 0.18, 0.28, 1.0),
        (0.22, 0.26, 0.38, 1.0),
    )

    # Day2: デバッグ
    DEBUG_ON_START: bool = False
