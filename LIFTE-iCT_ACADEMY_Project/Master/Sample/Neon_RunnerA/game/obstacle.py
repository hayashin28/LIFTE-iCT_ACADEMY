# -*- coding: utf-8 -*-
# 障害/コイン。見た目は四角で十分。

from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, StringProperty, ListProperty
from kivy.graphics import Color, Rectangle

class Obj(Widget):
    kind = StringProperty("ob")    # "ob" or "coin"
    vx   = NumericProperty(200.0)  # 左向き速度
    color= ListProperty([1,1,1,1])

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
