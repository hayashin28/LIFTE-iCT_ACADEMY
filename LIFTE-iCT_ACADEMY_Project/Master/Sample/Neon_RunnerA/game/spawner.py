# -*- coding: utf-8 -*-
# 出現を司る「状態付き」スポーナ。理不尽配置を避ける簡易ルールを実装。
import random
from kivy.core.window import Window

class SpawnState:
    """
    なぜ: フェアにゲームを進めるため、前回種類や残タスクを記憶しつつ次配置を決める。
    前提: 画面右外から左へ流す。dp変換は利用側（scenes）。
    出力: next_item() -> dict(kind,str; x,float; y,float; size,tuple(px,px))
    副作用: 内部に next_x, last_kind, train_remaining などの状態を持つ。
    """
    def __init__(self, P, ground_y_px, low_jump_h_px):
        self.P = P
        self.ground = ground_y_px
        self.low_h = low_jump_h_px
        # 次の配置X（画面右端より外）
        self.next_x = Window.width + random.uniform(0, P.SPAWN_SPREAD_PX)
        self.last_kind = None
        self.train_remaining = 0  # 連結の残り台数

    def _choose_kind(self):
        # 連結が進行中なら継続
        if self.train_remaining > 0:
            self.train_remaining -= 1
            return "ob_train"
        # 重み付きサンプリング（低/高/連結/コイン）
        w = [
            ("ob_low",   self.P.WEIGHT_OB_LOW),
            ("ob_high",  self.P.WEIGHT_OB_HIGH),
            ("ob_train", self.P.WEIGHT_OB_TRAIN),
            ("coin",     self.P.WEIGHT_COIN),
        ]
        r = random.random() * sum(v for _, v in w)
        acc = 0.0
        for k, v in w:
            acc += v
            if r <= acc:
                if k == "ob_train":
                    self.train_remaining = random.randint(self.P.TRAIN_SEGMENTS_MIN,
                                                          self.P.TRAIN_SEGMENTS_MAX) - 1
                return k
        return "ob_low"

    def next_item(self, speed):
        """
        1) ギャップを決定（高障害の直後は余裕を足す）
        2) 種別選択（必要なら連結継続）
        3) y/sizeを決めて辞書で返す
        """
        # 基本ギャップ
        gap = self.P.MIN_GAP_PX + random.uniform(0, self.P.SPAWN_SPREAD_PX)
        if self.last_kind == "ob_high":
            gap += self.P.EXTRA_GAP_AFTER_HIGH
        # 連結継続中なら短ギャップ
        if self.train_remaining > 0:
            gap = self.P.TRAIN_SEGMENT_GAP_PX

        self.next_x += gap
        kind = self._choose_kind()
        self.last_kind = kind

        # y/size 決定
        if kind == "coin":
            y = self.ground + self.low_h
            size = (28, 28)
        elif kind == "ob_high":
            y = self.ground
            size = (self.P.OB_HIGH_W, self.P.OB_HIGH_H)
        else:  # ob_low / ob_train
            y = self.ground
            size = (self.P.OB_LOW_W, self.P.OB_LOW_H)

        return {
            "kind": kind,
            "x": self.next_x,
            "y": y,
            "size": size,  # px
        }
