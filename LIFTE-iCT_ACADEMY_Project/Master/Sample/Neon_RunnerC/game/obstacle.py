# -*- coding: utf-8 -*-
"""
obstacle.py（障害物の最小モデル）
--------------------------------------------------------------------
■ なぜ / 目的
  - src 依存なしのサンプルとして、config を参照する軽量なロジックを用意。

■ 前提
  - ルートの config から速度の基準値を得る。

■ 入出力
  - 入力: コンストラクタで初期座標、update(dt) でフレーム時間（秒）。
  - 出力: 内部状態（x 座標）が更新される。

■ 副作用
  - なし（オブジェクト内部の値を変更するのみ）。

■ 例外
  - dt が負の場合、将来的には ValueError を投げても良い（今回は割愛）。
"""
from .. import config

class Obstacle:
    """
    横スクロール想定の単純な障害物。
    - 実ゲームではあたり判定やスプライト描画などを追加していきます。
    """
    def __init__(self, x: float = 0.0, y: float = 0.0) -> None:
        self.x = float(x)
        self.y = float(y)
        # 基準速度の 80% で左に流れるサンプル設定
        self.speed = float(config.PLAYER_SPEED) * 0.8

    def update(self, dt: float) -> None:
        """
        位置更新。
        :param dt: 経過時間（秒）
        """
        # 左方向（x マイナス）へ移動
        self.x -= self.speed * float(dt)
