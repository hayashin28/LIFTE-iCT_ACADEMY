# -*- coding: utf-8 -*-
# プレイヤーを四角形で表現。vy（縦速度）と地面クランプが肝。

from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, BooleanProperty, ListProperty
from kivy.graphics import Color, Rectangle

class Player(Widget):
    vy = NumericProperty(0.0)          # 上向き正の速度
    on_ground = BooleanProperty(True)  # 地面に接地中か
    color = ListProperty([0.2, 0.9, 1, 1])

    def __init__(self, **kw):
        super().__init__(**kw)
        with self.canvas:
            self._color = Color(*self.color)
            self._rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(pos=self._sync, size=self._sync, color=self._recolor)

    def _sync(self, *a):
        self._rect.pos = self.pos
        self._rect.size = self.size

    def _recolor(self, *a):
        self._color.rgba = self.color
