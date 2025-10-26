# -*- coding: utf-8 -*-
"""
ui/hud.py – デバッグ HUD の描画
なぜ: 位置や fps を可視化し、バグを詰まりにくくするため。
前提: Label で簡易表示。H キーで表示トグル。
入出力: 外部から set_info(dict) で値を受け取り、テキストに反映。
副作用: なし
例外: 文字化け防止のため ASCII 中心の表示に留める。
"""
from kivy.uix.label import Label
from kivy.properties import BooleanProperty

class DebugHUD(Label):
    visible = BooleanProperty(True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.markup = True
        self.font_size = "16sp"
        self.text = ""
        self.halign = "left"
        self.valign = "top"
        self.size_hint = (1, 1)
        self.padding = (8, 8)

    def set_info(self, info: dict):
        """info = dict(x=..., y=..., dir=..., fps=..., tile_x=..., tile_y=...)"""
        self.text = (
            "[b]HUD[/b]\\n"
            f"x={info.get('x',0):.1f}, y={info.get('y',0):.1f}, dir={info.get('dir','-')}\\n"
            f"tile=({info.get('tile_x',0)},{info.get('tile_y',0)})\\n"
            f"fps={info.get('fps',0):.1f}"
        )
        self.opacity = 1.0 if self.visible else 0.0
