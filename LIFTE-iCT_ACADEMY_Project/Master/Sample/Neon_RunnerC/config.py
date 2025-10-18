# -*- coding: utf-8 -*-
"""
config.py（設定値の集約）
--------------------------------------------------------------------
■ なぜ / 目的
  - ゲーム全体で共有する設定値（ウィンドウサイズ・スピードなど）を一カ所で管理して、
    参照・調整を容易にする。

■ 前提
  - パッケージから `from . import config` またはサブパッケージから `from .. import config` で参照。

■ 入出力 / 副作用 / 例外
  - 単なる定数定義のため特になし。
"""
APP_NAME: str = "Neon Runner C"
VERSION: str = "clean-1.2-jp"

WINDOW_WIDTH: int = 900
WINDOW_HEIGHT: int = 600

# ゲーム系の基本パラメータ
PLAYER_SPEED: float = 5.0  # プレイヤーの標準速度（px/sec のイメージ）
