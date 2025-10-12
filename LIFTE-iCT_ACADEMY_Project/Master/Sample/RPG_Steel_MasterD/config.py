# -*- coding: utf-8 -*-
"""
config.py – ゲーム全体の設定値（魔法値の追放）

なぜ: 画面サイズ・速度・タイルサイズなどを集中管理して、各所に散らばる「謎の定数」を無くすため。
前提: Kivy を前提にピクセル座標で描画。タイルサイズでマップと座標変換する。
入出力: なし（値を import して参照する）
副作用: なし
例外: 値の不整合（例: WIDTH/TILE が割り切れない）に注意。基本は偶数・割り切れる値にする。
"""
from pathlib import Path

# 画面サイズとタイル
WIDTH = 960
HEIGHT = 640
TILE = 32

# 移動速度（ピクセル/秒）— dt（秒）と乗算してフレーム移動量にする
SPEED = 150.0

# プレイヤーの当たり判定（半径または半サイズ）
# ここでは矩形半サイズ（px）。タイルサイズより少し小さめだと引っかかりにくい
PLAYER_HALF_W = 12
PLAYER_HALF_H = 12

# アセットパス
ASSETS_DIR = Path(__file__).resolve().parents[1] / "assets"
MAPS_DIR = ASSETS_DIR / "maps"
DEFAULT_MAP_CSV = MAPS_DIR / "field.csv"

# カラー（RGBA）
COLOR_BG = (0.08, 0.09, 0.12, 1.0)     # 背景
COLOR_PLAYER = (0.9, 0.9, 0.95, 1.0)   # プレイヤー
COLOR_WALL = (0.35, 0.38, 0.42, 1.0)   # 壁
COLOR_FLOOR = (0.18, 0.20, 0.24, 1.0)  # 床
COLOR_HUD = (0.95, 0.95, 0.95, 1.0)    # HUD 文字色
